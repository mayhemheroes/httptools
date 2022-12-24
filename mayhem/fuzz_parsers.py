#!/usr/bin/env python3

import atheris
import sys
import fuzz_helpers

with atheris.instrument_imports(include=["uefi_firmware"]):
    import httptools

parser_options = [httptools.HttpResponseParser, httptools.HttpRequestParser]

@atheris.instrument_func
def TestOneInput(data):
    fdp = fuzz_helpers.EnhancedFuzzedDataProvider(data)
    try:
        if fdp.ConsumeBool():
            parser = fdp.PickValueInList(parser_options)(None)
            parser.feed_data(fdp.ConsumeRemainingBytes())
        else:
            httptools.parse_url(fdp.ConsumeRandomBytes())
    except httptools.HttpParserError:
        return -1



def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
