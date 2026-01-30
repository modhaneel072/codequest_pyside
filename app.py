"""CodeQuest - Interactive Python Learning Application."""

import sys
import logging
from pathlib import Path

from PySide6.QtWidgets import QApplication

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.ui.main_window import MainWindow
from src.core.logging_config import setup_logging
from src.core.config import get_config

# Initialize logging
setup_logging(
    level=logging.INFO,
    log_file="logs/codequest.log",
    console=True
)

logger = logging.getLogger(__name__)


def main():
    """Main entry point for CodeQuest application."""
    try:
        logger.info("Starting CodeQuest application")
        
        # Load configuration
        config = get_config()
        logger.info(f"Application: {config.get('app.title')} v{config.get('app.version')}")
        
        # Create Qt application
        app = QApplication(sys.argv)
        
        # Create and show main window
        w = MainWindow()
        w.setWindowTitle(config.get('app.title', 'CodeQuest'))
        w.resize(
            config.get('app.window_width', 1200),
            config.get('app.window_height', 760)
        )
        w.show()
        
        logger.info("Application window created successfully")
        
        # Run application
        exit_code = app.exec()
        logger.info(f"Application exited with code {exit_code}")
        return exit_code
        
    except Exception as e:
        logger.error(f"Fatal error during startup: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    sys.exit(main())
