type LogLevel = "debug" | "info" | "warn" | "error";

function writeLog(level: LogLevel, message: string, detail?: unknown) {
  const prefix = `[RecallTabs:${level.toUpperCase()}]`;

  if (detail === undefined) {
    console[level](prefix, message);
    return;
  }

  console[level](prefix, message, detail);
}

export const logger = {
  debug: (message: string, detail?: unknown) => writeLog("debug", message, detail),
  info: (message: string, detail?: unknown) => writeLog("info", message, detail),
  warn: (message: string, detail?: unknown) => writeLog("warn", message, detail),
  error: (message: string, detail?: unknown) => writeLog("error", message, detail),
};
