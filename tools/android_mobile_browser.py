"""Launch a web page with Android-like browser characteristics.

This script uses Playwright to start a Chromium instance configured to mimic an
Android device (Google Pixel 5). User agent, viewport, device scale factor and
touch support all match the mobile profile so that the visited page cannot
distinguish it from a phone browser.

Usage:
    python tools/android_mobile_browser.py https://example.com

Optional flags:
    --headless   Run without opening a visible window.

Prerequisites:
    pip install playwright
    playwright install chromium
"""

import argparse
from playwright.sync_api import sync_playwright


def launch_android_page(url: str, headless: bool = False) -> None:
    """Open ``url`` in a Chromium session emulating an Android handset."""
    with sync_playwright() as playwright:
        device = playwright.devices["Pixel 5"]

        browser = playwright.chromium.launch(headless=headless)
        context = browser.new_context(
            user_agent=device["user_agent"],
            viewport=device["viewport"],
            device_scale_factor=device["device_scale_factor"],
            is_mobile=device["is_mobile"],
            has_touch=device["has_touch"],
        )

        page = context.new_page()
        page.goto(url, wait_until="networkidle")

        print(
            "Navegador listo. Presiona Ctrl+C para cerrarlo cuando termines."
        )
        try:
            page.wait_for_timeout(60 * 60 * 1000)
        finally:
            context.close()
            browser.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Abre una página con un perfil de navegador Android realista "
            "utilizando Playwright."
        )
    )
    parser.add_argument(
        "url",
        help="Dirección a cargar con la emulación móvil (incluye https://)",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Ejecuta el navegador sin ventana visible.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    launch_android_page(args.url, headless=args.headless)
