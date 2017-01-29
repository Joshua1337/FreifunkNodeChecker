# coding: utf-8 
import logging
import argparse
from checkForUpdates import Check
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', filename="error.log")

stderr = logging.StreamHandler()
stderr.setFormatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logging.getLogger().addHandler(stderr)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Überprüft eine JSON-Datei nach Änderungen")
    parser.add_argument("-token", type=str, required=True, help="Authtoken für den Telegram Bot")
    parser.add_argument("-url", type=str, required=True, help="Netzwerkpfad zur JSON-Datei")
    parser.add_argument("-chat", type=int, required=True,
                        help="Telegram Chat-ID an die die Benachrichtigung gesendet werden soll")
    parsed_args = parser.parse_args()

    if not parsed_args.token:
        parser.print_help()
        exit()

    try:
        Check(parsed_args.token, parsed_args.url, parsed_args.chat).run()
    except Exception as e:
        logging.exception("brudi, es gab nen fehler")
