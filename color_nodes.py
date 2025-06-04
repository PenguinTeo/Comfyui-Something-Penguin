"""Simple color adjustment nodes for ComfyUI.

The environment used for this repository does not provide external image
processing libraries such as Pillow or OpenCV.  The nodes implemented here
therefore operate on images represented as lists of rows where each row is a
list of ``(R, G, B)`` tuples with channels in the range ``0``-``255``.  The
implementations are intentionally lightweight so that they work with nothing
but the Python standard library.  For real-world scenarios you would replace
these routines with versions that leverage proper image libraries.
"""

from typing import Any


class BrightnessContrastNode:
    """Adjust brightness and contrast of an image."""

    def __init__(self, brightness: float = 0.0, contrast: float = 1.0) -> None:
        self.brightness = brightness
        self.contrast = contrast

    def _adjust_channel(self, value: float) -> int:
        value = (value + self.brightness) * self.contrast
        return max(0, min(255, int(value)))

    def process(self, image: Any) -> Any:
        """Apply brightness/contrast to an ``image`` represented as nested lists."""

        return [
            [
                tuple(self._adjust_channel(c) for c in pixel)
                for pixel in row
            ]
            for row in image
        ]


class LevelsNode:
    """Perform a simple levels adjustment."""

    def __init__(self, black_point: float = 0.0, white_point: float = 255.0) -> None:
        self.black_point = black_point
        self.white_point = white_point if white_point != black_point else black_point + 1

    def _adjust_channel(self, value: float) -> int:
        scaled = (value - self.black_point) * 255 / (self.white_point - self.black_point)
        return max(0, min(255, int(scaled)))

    def process(self, image: Any) -> Any:
        """Scale channel values between ``black_point`` and ``white_point``."""

        return [
            [
                tuple(self._adjust_channel(c) for c in pixel)
                for pixel in row
            ]
            for row in image
        ]


class HueSaturationNode:
    """Modify hue and saturation using the :mod:`colorsys` helpers."""

    def __init__(self, hue: float = 0.0, saturation: float = 1.0) -> None:
        self.hue = hue
        self.saturation = saturation

    def _adjust_pixel(self, pixel: Any) -> Any:
        import colorsys

        r, g, b = [c / 255 for c in pixel]
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        h = (h + self.hue) % 1.0
        s = max(0.0, min(1.0, s * self.saturation))
        r2, g2, b2 = colorsys.hsv_to_rgb(h, s, v)
        return (int(r2 * 255), int(g2 * 255), int(b2 * 255))

    def process(self, image: Any) -> Any:
        """Apply hue and saturation adjustments to ``image``."""

        return [
            [self._adjust_pixel(pixel) for pixel in row]
            for row in image
        ]


class ColorBalanceNode:
    """Shift the colour balance of shadows, midtones and highlights."""

    def __init__(self,
                 shadows: tuple[int, int, int] = (0, 0, 0),
                 midtones: tuple[int, int, int] = (0, 0, 0),
                 highlights: tuple[int, int, int] = (0, 0, 0)) -> None:
        self.shadows = shadows
        self.midtones = midtones
        self.highlights = highlights

    def _apply_shift(self, pixel: tuple[int, int, int], shift: tuple[int, int, int]) -> tuple[int, int, int]:
        return tuple(
            max(0, min(255, c + s))
            for c, s in zip(pixel, shift)
        )

    def process(self, image: Any) -> Any:
        """Apply simple tonal colour shifts."""

        result = []
        for row in image:
            new_row = []
            for pixel in row:
                luminance = sum(pixel) / 3
                if luminance < 85:
                    new_row.append(self._apply_shift(pixel, self.shadows))
                elif luminance < 170:
                    new_row.append(self._apply_shift(pixel, self.midtones))
                else:
                    new_row.append(self._apply_shift(pixel, self.highlights))
            result.append(new_row)
        return result


class PerspectiveTransformNode:
    """Apply a perspective transformation to an image."""

    def __init__(self, matrix: Any) -> None:
        self.matrix = matrix

    def process(self, image: Any) -> Any:
        """Apply the perspective transform.

        This placeholder performs no transformation because a real
        perspective warp would require interpolation routines that
        depend on external libraries.
        """
        return image
