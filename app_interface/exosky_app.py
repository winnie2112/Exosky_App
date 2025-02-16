"""Gui app entry point."""

import sys
from pathlib import Path

import numpy as np
import numpy.typing as npt
import plotly.io as pio
from PySide6.QtCore import Property, QObject, QSize, QUrl, Signal, Slot
from PySide6.QtGui import QGuiApplication, QImage
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuick import QQuickImageProvider

from backend.exosky_backend import (
    CreateStarChart,
    ExoSkyBackend,
    SelectionPlanet,
    ThreeDStarChart,
)

CURRENT_DIRECTORY = Path(__file__).resolve().parent


class ImageProvider(QQuickImageProvider):
    """Signals for changing the displayed image."""

    def __init__(self) -> None:
        """Initialize class."""
        super(ImageProvider, self).__init__(  #  pylint: disable= [super-with-arguments]
            QQuickImageProvider.Image,  # type: ignore
        )
        self._image = None

    # pylint: disable=unused-argument
    def requestImage(self, id: str, size: QSize, requestedSize: QSize) -> QImage:
        """Update the to-be-displayed image."""
        return self._image  # type: ignore

    def set_image(self, image: QImage) -> None:
        """Setter."""
        self._image = image.copy()  # type: ignore


class EarthNightSky(QObject):
    """Display parameters of planet from Python backend on QML interface."""

    earth_nightsky_changed = Signal()
    update_earth_nightsky = Signal()

    threed_nightsky_changed = Signal(str)

    def __init__(self, parent: QObject | None = None) -> None:
        """Initialize class."""
        super().__init__(parent)
        self._earth_nightsky: QImage = QImage()
        self._threed_nightsky: str = ""

    def set_earth_nightsky(self, image: QImage) -> None:
        """Set stars from Earth's pov cone to the target exoplanet."""
        self._earth_nightsky = image
        self.earth_nightsky_changed.emit()

    @Property(  # type: ignore
        QImage, notify=earth_nightsky_changed, fset=set_earth_nightsky, constant=False  # type: ignore
    )
    def get_earth_nightsky(self) -> QImage:
        """Get stars from Earth's pov cone to the target exoplanet."""
        return self._earth_nightsky

    @Slot(dict, dict)
    def create_star_chart(
        self,
        select_exoplanet: SelectionPlanet,
        star_chart: CreateStarChart,
    ) -> None:
        """Have backend display stars within Earth/exoplanet cone."""
        exo_planet = ExoSkyBackend().create_star_chart(select_exoplanet, star_chart)
        qexo_planet = to_q_image(exo_planet)
        # do we need to convert to QImage, when we can just pass the json str like 3D graph?
        # to be improved...
        self.set_earth_nightsky(qexo_planet)

    def set_threed_nightsky(self, msg: str) -> None:
        """Set threed_nightsky."""
        self._threed_nightsky = msg
        self.threed_nightsky_changed.emit(msg)

    @Property(  # type: ignore
        str,
        fset=set_threed_nightsky,
        notify=threed_nightsky_changed,  # type: ignore
    )
    def get_threed_nightsky(self) -> str:
        """Get threed_nightsky."""
        return self._threed_nightsky

    @Slot(dict, dict)
    def create_threed_star_chart(
        self,
        select_exoplanet: SelectionPlanet,
        threed_star_chart: ThreeDStarChart,
    ) -> None:
        """Have backend display stars in 3D within Earth/exoplanet cone."""
        fig = ExoSkyBackend().create_threed_star_chart(
            select_exoplanet, threed_star_chart
        )
        json_str = pio.to_json(fig)
        self.set_threed_nightsky(json_str)


class ExoSkyApp(QGuiApplication):
    """Bridge for creating exosky app."""

    def __init__(self) -> None:
        """Initialize ExoSkyBakend app."""
        super().__init__()
        name = "Exosky App"
        self.setApplicationDisplayName(name)

        self.earth_pov = EarthNightSky()
        self.provider = ImageProvider()

        self.engine = QQmlApplicationEngine()
        self.engine.rootContext().setContextProperty("earthnightsky", self.earth_pov)
        self.engine.addImageProvider("provider", self.provider)
        self.engine.load(QUrl.fromLocalFile(str(CURRENT_DIRECTORY / "main.qml")))

        self.earth_pov.earth_nightsky_changed.connect(self.display_stars_from_earth)

    def display_stars_from_earth(self) -> None:
        """Give signal, how Earth nightsky would look like toward the target exoplanet."""
        stars_earth_cone = self.earth_pov.get_earth_nightsky
        self.provider.set_image(stars_earth_cone)
        self.earth_pov.update_earth_nightsky.emit()


def to_q_image(image: npt.NDArray[np.uint8] | npt.NDArray[np.uint16]) -> QImage:
    """Convert to QImage."""
    height, width = image.shape[:2]
    if image.ndim == 2:
        # Grayscale image
        image_format = (
            QImage.Format_Grayscale8
            if image.dtype == np.uint8
            else QImage.Format_Grayscale16
        )
        q_image = QImage(image.data, width, height, width, image_format)
    elif image.ndim == 3:
        if image.shape[2] == 3:
            # RGB image
            image_format = (
                QImage.Format_RGB888
                if image.dtype == np.uint8
                else QImage.Format_RGB444
            )
            q_image = QImage(image.data, width, height, width * 3, image_format)
        elif image.shape[2] == 4:
            # RGBA image
            image_format = (
                QImage.Format_RGBA8888
                if image.dtype == np.uint8
                else QImage.Format_RGB444
            )
            q_image = QImage(image.data, width, height, width * 4, image_format)
    else:
        raise ValueError("Unsupported image format")
    return q_image


def main() -> None:
    """App entry point."""
    app = ExoSkyApp()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
