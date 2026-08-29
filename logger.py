import logging
import re

class Redact(logging.Filter):
    def filter(self, record):
        record.msg = re.sub(r"(?i)(session|secret|token)\s*[:=]\s*[^\s]+", r"\1=[REDACTED]", str(record.msg))
        return True

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
log = logging.getLogger("taskbot")
log.addFilter(Redact())
