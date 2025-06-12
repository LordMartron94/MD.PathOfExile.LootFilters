from md_pathofexile_lootfilters.components.md_common_python.py_common.logging import HoornLoggerBuilder, HoornLogger, \
    LogType
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.app import App
from md_pathofexile_lootfilters.components.md_pathofexile_lootfilters.constants import APP_NAME, MAX_SEPARATOR_LENGTH, \
    DEBUG_MODE, VERBOSE

logger_builder: HoornLoggerBuilder = HoornLoggerBuilder(
    application_name_sanitized=APP_NAME,
    max_separator_length=MAX_SEPARATOR_LENGTH
)

(logger_builder
 .build_gui_output(base_batch_size=1000, max_batch_size=5000)
 .build_file_based_output(
    max_logs_to_keep=25
))

min_log: LogType = LogType.TRACE \
    if (DEBUG_MODE and VERBOSE) \
    else LogType.DEBUG \
        if DEBUG_MODE \
    else LogType.INFO

if __name__ == "__main__":
    logger: HoornLogger = logger_builder.get_logger(min_level=min_log)

    app: App = App(logger)

    app.run()
