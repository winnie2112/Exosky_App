"""Backend for exosky interface. 

This scirpt is suppose to be a cleaner backend version of messy_coordinate_transformation.ipynb.
Check out jupyter notebook for the full calculation."""

import io
from typing import Dict, TypedDict, Tuple

import os
from pathlib import Path
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
import pandas as pd
import PIL
from astropy import units as u
from astropy.coordinates import Distance, SkyCoord
from astropy.table import QTable, Table
from astropy.coordinates import Angle
from astroquery.ipac.nexsci.nasa_exoplanet_archive import NasaExoplanetArchive
from astroquery.gaia import Gaia
import plotly.graph_objects as go


matplotlib.use("Agg")


class SelectionPlanet(TypedDict):
    """Allow the user to select planet."""

    planet: str
    checked_earth_pov: bool

class CreateStarChart(TypedDict):
    """Allow the user to view how stars can be displayed."""

    star_size: int | float
    magnitude_limit: int | float
    fov: int | float

class ThreeDStarChart(TypedDict):
    """Allow the user to view 3D star chart."""

    number_of_stars: int
    star_size_perspective: int | float

def query_exoplanets(export_path) -> pd.DataFrame:
    """Query nearly 5740 exoplanets and export it to query_exoplanets.csv
    
    Planet name, right ascension, declination, parallax & distance from NASA exoplanet archive.
    """
    results_exoplanets = NasaExoplanetArchive.query_criteria(
                            table="pscomppars", 
                            select="pl_name, ra, dec, sy_plx, sy_dist", 
                            where="sy_dist is not Null", 
                            order="sy_dist"
                        )
    df_exoplanets = results_exoplanets.to_pandas()
    df_exoplanets.to_csv(export_path, index=False)
    return df_exoplanets

def read_planet_data(
    select_exoplanet: SelectionPlanet,
    exoplanets: str = r"resources\table_data\query_exoplanets.csv.gz",
) -> Dict:
    """Get corresponding planet data from compressed query_exoplanets.csv."""
    # reading the csv file is faster than querying the data again
    planet_path = pd.read_csv(exoplanets)
    planet_data = planet_path[planet_path["pl_name"] == select_exoplanet["planet"]].iloc[0]

    return {
        "exoplanet": planet_data["pl_name"],
        "planet_ra": planet_data["ra"],
        "planet_dec": planet_data["dec"],
        "planet_sy_dist": planet_data["sy_dist"],
        "planet_sy_plx": planet_data["sy_plx"],
    }

def query_stars_earth_pov(select_exoplanet: SelectionPlanet, export_path: str) -> pd.DataFrame:
    """Query the stars within the path from Earth to the target exoplanet
    
    star name, right ascension, declination, parallax & distance from Gaia.
    """
    example_ra = read_planet_data(select_exoplanet)["planet_ra"]
    example_dec = read_planet_data(select_exoplanet)["planet_dec"]
    query_stars = """
    SELECT TOP 500000 gaia_source.designation,gaia_source.ra,gaia_source.dec,gaia_source.parallax,gaia_source.phot_g_mean_mag,gaia_source.distance_gspphot
    FROM gaiadr3.gaia_source
    WHERE parallax IS NOT NULL
    AND CONTAINS(
        POINT("ICRS",gaiadr3.gaia_source.ra,gaiadr3.gaia_source.dec),
        CIRCLE("ICRS",""" + str(example_ra) + """,""" + str(example_dec)+ """,90)
    )=1
    AND  (gaiadr3.gaia_source.phot_g_mean_mag<10)
    ORDER BY gaia_source.distance_gspphot ASC
    """

    job_stars = Gaia.launch_job(query_stars)
    stars_from_earth_cone = job_stars.get_results()
    df_stars_from_earth_cone = stars_from_earth_cone.to_pandas()
    df_stars_from_earth_cone.to_csv(export_path, index=False)
    return df_stars_from_earth_cone

def query_stars_exoplanet_pov(select_exoplanet: SelectionPlanet, export_path: str) -> pd.DataFrame:
    """Query the stars within the path from the target exoplanet onwards.
    
    Stars from Earth to this plant won"t be included.
    """
    example_ra = read_planet_data(select_exoplanet)["planet_ra"]
    example_dec = read_planet_data(select_exoplanet)["planet_dec"]
    example_sy_dist = read_planet_data(select_exoplanet)["planet_sy_dist"]
    example_sy_plx = read_planet_data(select_exoplanet)["planet_sy_plx"]

    lower_bound = 1 * u.lyr
    upper_bound = 1 * u.lyr

    lower_bound_plx = lower_bound.to(u.mas, equivalencies=u.parallax())
    upper_bound_plx = upper_bound.to(u.mas, equivalencies=u.parallax())

    # distance in parsec (1pc = 3.26ly)
    distance_minimum = example_sy_dist - (lower_bound).value
    distance_maximum = example_sy_dist + (upper_bound).value

    # parallax as fallback as some stars don"t have any distance values (1 parsec = 1 arcsecond)
    parallax_minimum = example_sy_plx - (lower_bound_plx).value
    parallax_maximum = example_sy_plx + (upper_bound_plx).value

    query_stars_filtered ="""
    SELECT TOP 500000 gaia_source.designation,gaia_source.ra,gaia_source.dec,gaia_source.parallax,gaia_source.phot_g_mean_mag,gaia_source.distance_gspphot
    FROM gaiadr3.gaia_source
    WHERE
    CONTAINS(
        POINT("ICRS",gaiadr3.gaia_source.ra,gaiadr3.gaia_source.dec),
        CIRCLE("ICRS",""" + str(example_ra) + """,""" + str(example_dec)+ """,90)
    )=1  AND  ((gaiadr3.gaia_source.distance_gspphot BETWEEN """+ str(distance_minimum)+""" AND """ + str(distance_maximum) + """) OR (gaiadr3.gaia_source.parallax BETWEEN""" + str(parallax_minimum)+""" AND """ + str(parallax_maximum) + """))
    ORDER BY gaia_source.distance_gspphot ASC, gaia_source.parallax ASC
    """
    job_stars_filtered = Gaia.launch_job(query_stars_filtered)
    results_stars_filtered = job_stars_filtered.get_results()
    df_results_stars_filtered = results_stars_filtered.to_pandas()
    df_results_stars_filtered.to_csv(export_path, index=False)

    return df_results_stars_filtered

def read_star_data(select_exoplanet: SelectionPlanet) -> Dict:
    """Read star data from the exported csv file."""

    planet_files = {
        "TOI-700 d": (
            r"resources\table_data\stars_from_earth_pov_radius90\query_stars_earth_to_toi-700d_cone.csv.gz",
            r"resources\table_data\stars_from_exoplanet_pov_radius90\query_stars_from_toi-700d_cone.csv.gz"
        ),
        "Ross 128 b": (
            r"resources\table_data\stars_from_earth_pov_radius90\query_stars_earth_to_ross-128b_cone.csv.gz",
            r"resources\table_data\stars_from_exoplanet_pov_radius90\query_stars_from_ross-128b_cone.csv.gz"
        ),
        "TRAPPIST-1 e": (
            r"resources\table_data\stars_from_earth_pov_radius90\query_stars_earth_to_trappist-1e_cone.csv.gz",
            r"resources\table_data\stars_from_exoplanet_pov_radius90\query_stars_from_trappist-1e_cone.csv.gz"
        )
    }

    query_stars_from_earth_cone, query_stars_from_planet_cone = planet_files.get(select_exoplanet["planet"], (None, None))

    from_earth_cone = pd.read_csv(query_stars_from_earth_cone)
    from_planet_cone = pd.read_csv(query_stars_from_planet_cone)

    return {
        "stars_from_earth_cone": from_earth_cone,
        "earth_cone_ra": from_earth_cone["ra"],
        "earth_cone_dec": from_earth_cone["dec"],
        "earth_cone_parallax": from_earth_cone["parallax"],
        "earth_cone_mag": from_earth_cone["phot_g_mean_mag"],
        "earth_cone_gspphot": from_earth_cone["distance_gspphot"],

        "stars_from_exo_cone": from_planet_cone,
        "exo_cone_ra": from_planet_cone["ra"],
        "exo_cone_dec": from_planet_cone["dec"],
        "exo_cone_parallax": from_planet_cone["parallax"],
        "exo_cone_mag": from_planet_cone["phot_g_mean_mag"],
        "exo_cone_gspphot": from_planet_cone["distance_gspphot"],
    }

def prepare_star_data(
    select_exoplanet: SelectionPlanet,
    star_chart: CreateStarChart,
) -> Dict:
    """Select the stars within the FOV of Earth to target Exoplanet.

    Read the stars from query cone search from Gaia.
    The exoplanet is at the center of Earth"s field of view.
    Cone has a radius of 90 degrees.
    """
    exoplanet_ra = read_planet_data(select_exoplanet)["planet_ra"]
    exoplanet_dec = read_planet_data(select_exoplanet)["planet_dec"]

    star_data = read_star_data(select_exoplanet)

    if select_exoplanet["checked_earth_pov"]:
        stars = star_data["stars_from_earth_cone"]
        star_ra = star_data["earth_cone_ra"]
        star_dec = star_data["earth_cone_dec"]
    else:
        stars = star_data["stars_from_exo_cone"]
        star_ra = star_data["exo_cone_ra"]
        star_dec = star_data["exo_cone_dec"]
    
    # view stars within a specific field of view
    lower_ra = exoplanet_ra - star_chart["fov"] / 2
    upper_ra = exoplanet_ra + star_chart["fov"] / 2
    lower_dec = exoplanet_dec - star_chart["fov"] / 2
    upper_dec = exoplanet_dec + star_chart["fov"] / 2

    mask = (
        (star_ra > lower_ra)
        & (star_ra < upper_ra)
        & (star_dec > lower_dec)
        & (star_dec < upper_dec)
    )
    filtered_stars = stars[mask]

    return {
        "stars_Earth_exo": filtered_stars,
        "stars_upper_half": upper_ra,
        "stars_lower_half": lower_ra,
    }

def galactic_to_cartesian(ra, dec, parallax) -> SkyCoord:
    """Convert galactic coordinates to Cartesian coordinates.
    
    param ra: Right ascension in degrees.
    param dec: Declination in degrees.
    param parallax: Distance in parsecs. Parallax is the apparent shift in the position of an object when observed from different viewpoints.
    """
    return SkyCoord(ra = Angle(ra, unit=u.deg),
                    dec = Angle(dec, unit=u.deg),
                    distance= parallax * u.pc).represent_as("cartesian")

def shift_coordinates(ras, decs, parallaxes,phi0, theta0, r0):
    """
    Shifts the given coordinates by the specified reference point in galactic coordinates.
    Parameters:
    ras (array-like): Right ascensions of the objects.
    decs (array-like): Declinations of the objects.
    parallaxes (array-like): Parallaxes of the objects.
    phi0 (float): Right ascension of the reference point.
    theta0 (float): Declination of the reference point.
    r0 (float): Parallax of the reference point.
    """

    coord_exo_stars = galactic_to_cartesian(ras, decs, parallaxes)
    coord_planets = galactic_to_cartesian(phi0, theta0, r0)
    x_new = coord_exo_stars.x - coord_planets.x.value
    y_new = coord_exo_stars.y - coord_planets.y.value
    z_new = coord_exo_stars.z - coord_planets.z.value
    
    coords_cartesian = SkyCoord(x_new, y_new, z_new, representation_type='cartesian')
    coords_spherical = coords_cartesian.represent_as('spherical')

    return coords_spherical, coords_cartesian

def calculate_distances_cartesian(x,y,z):
    """Calculate the distance of the stars from the origin."""
    return np.sqrt(x**2 + y**2 + z**2)

class ExoSkyBackend:
    """Backend to display star charts."""
    def __init__(self) -> None:
        """Initialize the backend."""

    def create_star_chart(
        self,
        select_exoplanet: SelectionPlanet,
        star_chart: CreateStarChart,
    ):
        """Star chart from Earth point of view.

        The center of the chart is the target exoplanet.
        """
        exo_name = read_planet_data(select_exoplanet)["exoplanet"]
        exo_ra = read_planet_data(select_exoplanet)["planet_ra"]
        exo_dec = read_planet_data(select_exoplanet)["planet_dec"]

        star_data = prepare_star_data(select_exoplanet, star_chart)
        stars_earth_exo = star_data["stars_Earth_exo"]
        x_lim_lower = star_data["stars_lower_half"]
        x_lim_upper = star_data["stars_upper_half"]

        # filter stars based on input magnitude
        brighter_stars = stars_earth_exo["phot_g_mean_mag"] <= star_chart["magnitude_limit"]
        magnitude = stars_earth_exo["phot_g_mean_mag"][brighter_stars]

        # adjust size of marker based on magnitude
        marker_size = 10 ** (magnitude / -2.5) * star_chart["star_size"]

        # plot stars
        plt.figure(figsize=(8, 8), facecolor="#041A40")
        plt.scatter(
            stars_earth_exo["ra"][brighter_stars],
            stars_earth_exo["dec"][brighter_stars],
            s=marker_size,
            color="white",
            marker=".",
            zorder=2,
        )

        if select_exoplanet["checked_earth_pov"]:
            circle = plt.Circle(
                (exo_ra, exo_dec),
                radius=0.3,
                color="red",
                fill=False,
                linewidth=2,
                zorder=1,
            )
            plt.gca().add_patch(circle)
            plt.text(
                exo_ra + 0.5,
                exo_dec,
                exo_name,
                color="yellow",
                fontsize=10,
                ha="left",
                va="center",
            )
            target_planet = "Earth"
        else:
            target_planet = exo_name

        plt.gca().set_facecolor("black")
        plt.gca().set_aspect("equal")
        plt.xlim(x_lim_lower, x_lim_upper)
        plt.margins(x=0, y=0)
        plt.xticks(color="white")
        plt.yticks(color="white")
        plt.xlabel("Right Ascension", color="white")
        plt.ylabel("Declination", color="white")
        plt.title(f"Star Chart from {target_planet} with fov of {star_chart["fov"]}", color="yellow")
        
        # Convert plot to numpy array
        buf = io.BytesIO()
        plt.savefig(buf, format="png", bbox_inches="tight", pad_inches=0.2, dpi=300)
        buf.seek(0)
        nightsky = PIL.Image.open(buf)
        plt.close()
        return np.array(nightsky)

    def create_threed_star_chart(
        self,
        select_exoplanet: SelectionPlanet,
        threed_star_chart: ThreeDStarChart,
    ) -> go.Figure:
        """Plot 3D star chart and return the path to the HTML file."""
        # Take only the stars within the FOV of exoplanet and convert to Cartesian coordinates
        
        exo_cone_ra = read_star_data(select_exoplanet)["exo_cone_ra"]
        exo_cone_dec = read_star_data(select_exoplanet)["exo_cone_dec"]
        exo_cone_parallax = read_star_data(select_exoplanet)["exo_cone_parallax"]
        exo_cone_gspphot = read_star_data(select_exoplanet)["exo_cone_gspphot"]
        exo_cone_mag = read_star_data(select_exoplanet)["exo_cone_mag"]
        

        planet_ra = read_planet_data(select_exoplanet)["planet_ra"]
        planet_dec = read_planet_data(select_exoplanet)["planet_dec"]
        planet_sy_dist = read_planet_data(select_exoplanet)["planet_sy_dist"]

        fig = go.Figure()

        if select_exoplanet["checked_earth_pov"]:

            _, cartesian_exo_stars_coords = shift_coordinates(
                                        exo_cone_ra,
                                        exo_cone_dec,
                                        exo_cone_parallax,
                                        planet_ra,
                                        planet_dec,
                                        planet_sy_dist,
                                    )
            # calculate absolute magnitude
            exo_cone_mag = np.nan_to_num(exo_cone_mag, nan=2.5)
            stars_abs_magnitude = exo_cone_mag - 5 * np.log(exo_cone_parallax - 1)

            gspphot = calculate_distances_cartesian(cartesian_exo_stars_coords.x,
                                                    cartesian_exo_stars_coords.y,
                                                    cartesian_exo_stars_coords.z)

            # recalculate apparent magnitude
            stars_re_abs_mag = stars_abs_magnitude - 5 * np.log(np.abs(gspphot - 1))
            marker_size = (1 / 100) * 10 ** (stars_re_abs_mag / -2.5)

            fig.add_trace(go.Scatter3d( # convert the value to list to display on QML
                x=cartesian_exo_stars_coords[:threed_star_chart["number_of_stars"]].x.value.tolist(),
                y=cartesian_exo_stars_coords[:threed_star_chart["number_of_stars"]].y.value.tolist(),
                z=cartesian_exo_stars_coords[:threed_star_chart["number_of_stars"]].z.value.tolist(),
                mode="markers",
                name="Stars",
                marker=dict(
                    size= marker_size[:threed_star_chart["number_of_stars"]].tolist(),
                    color="white",
                )
            ))

            fig.add_trace(go.Scatter3d(
                x=[0],
                y=[0],
                z=[0],
                mode="markers+text",
                name=f"{select_exoplanet["planet"]}",
                marker=dict(size=5, color="red"),
                text=f"{select_exoplanet["planet"]}",
                textposition="top center"
            ))

        else:

            earth_stars_coords = galactic_to_cartesian(
                exo_cone_ra,
                exo_cone_dec,
                exo_cone_gspphot,
            )

            # fabricate nan value of star magnitude and keep the same data length
            exo_cone_mag = np.nan_to_num(exo_cone_mag, nan=2.5)
            marker_size = 10 ** (exo_cone_mag / -2.5) * threed_star_chart["star_size_perspective"]
                
            fig.add_trace(go.Scatter3d( # convert the value to list to display on QML
                x=earth_stars_coords[:threed_star_chart["number_of_stars"]].x.value.tolist(),
                y=earth_stars_coords[:threed_star_chart["number_of_stars"]].y.value.tolist(),
                z=earth_stars_coords[:threed_star_chart["number_of_stars"]].z.value.tolist(),
                mode="markers",
                name="Stars",
                marker=dict(
                    size= marker_size[:threed_star_chart["number_of_stars"]].tolist(),
                    color="white",
                )
            ))

            planets_coords = galactic_to_cartesian(planet_ra, planet_dec, planet_sy_dist)

            fig.add_trace(go.Scatter3d(
                x=[0],
                y=[0],
                z=[0],
                mode="markers+text",
                name="Earth",
                marker=dict(size=2, color="blue"),
                text=["Earth"],
                textposition="top center"
            ))

            fig.add_trace(go.Scatter3d(
                x=[planets_coords.x.value],
                y=[planets_coords.y.value],
                z=[planets_coords.z.value],
                mode="markers+text",
                name= f"{select_exoplanet["planet"]}",
                marker=dict(size=5, color="red"),
                text=[select_exoplanet["planet"]],
                textposition="top center"
            ))

        fig.update_layout(scene=dict(
            xaxis=dict(showbackground=False, showgrid=False, zeroline=False),#, showticklabels=False),
            yaxis=dict(showbackground=False, showgrid=False, zeroline=False),#, showticklabels=False),
            zaxis=dict(showbackground=False, showgrid=False, zeroline=False),#, showticklabels=False),
            bgcolor="black"
        ),

        paper_bgcolor="black",
        plot_bgcolor="black",
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.1,
            xanchor="center",
            x=0.5,
            title=None,
            itemsizing="constant"
        ))
        fig.show()
        return fig

if __name__ == "__main__":
    # test if functions work like I wanted to
    data = SelectionPlanet(
        planet="TOI-700 d",
        checked_earth_pov=True,
    )
    star_infos = CreateStarChart(
        star_size=100,
        magnitude_limit=200,
        fov=30,
    )
    threed_star_infos = ThreeDStarChart(
        number_of_stars=49999,
        star_size_perspective=100,
    )
    # ra = read_star_data(data)["earth_cone_ra"]
    # star_test = prepare_star_data(data, star_infos)
    # image = ExoSkyBackend().star_chart_from_earth(data, star_infos)
    #plt.imshow(image)
    #plt.show()
    ExoSkyBackend().create_threed_star_chart(data, threed_star_infos)
    print("Done!")
