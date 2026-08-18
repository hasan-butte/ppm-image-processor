# PPM Image Processor

A PPM (P3) image reader/writer/filter tool implemented in two paradigms:
C++ using an object-oriented approach, and Python using a procedural
approach. Built to compare how each paradigm handles the same problem.

## Features

Both implementations support:
- Grayscale conversion
- Color inversion
- Horizontal flip
- 8-bit color normalization (for source images with a max color value other than 255)
- Input validation and error handling

A written report comparing the two paradigms' tradeoffs in maintainability,
writability, and reliability is included in [`report/`](./report).

## Repo structure

```
.
├── cpp/
│   ├── Image.h            # Abstract base class: shared state, filters, read/write interface
│   ├── Image.cpp
│   ├── PPMImage.h         # Concrete subclass, implements PPM-specific read/write
│   ├── PPMImage.cpp
│   └── ppm_csolution.cpp  # Entry point (interactive CLI)
├── python/
│   └── ppm_psolution.py   # Procedural implementation (dict-based reader/writer/filter dispatch)
├── tests/
│   ├── input/              # Sample PPM images used for testing
│   ├── output_cpp/         # C++ output lands here when you run it
│   ├── output_python/      # Python output lands here when you run it
│   └── output_solutions/   # Precomputed reference outputs for all 3 images x 3 filters
├── report/                 # Paradigm tradeoff analysis
├── run.py                  # Convenience runner for both implementations
└── README.md
```

## Design notes

The C++ implementation is built around an abstract `Image` base class that
holds shared state (width, height, pixel array) and the filter logic
(`grayscale`, `invert`, `hflip`) directly, with a pure virtual `read`/`write`
interface. `PPMImage` is a concrete subclass that implements the
format-specific parsing and serialization. The filters don't need to know
or care what file format the pixels came from.

The Python implementation takes a procedural approach instead: standalone
functions for reading, writing, and each filter, with `READERS`/`WRITERS`
dictionaries mapping format strings to functions and a `METHODS` dictionary
mapping menu choices to filter functions. There's no class hierarchy here.
Format extensibility comes from adding entries to the dispatch dictionaries
rather than adding subclasses.

## Requirements

- A C++17-compatible compiler (`g++`)
- Python 3

## Running it

From the repo root:

```
python run.py
```

You'll be asked to choose C++ or Python. Choosing C++ compiles the sources
with `g++ -std=c++17 -O2` automatically if the binary is missing or stale,
then runs it; choosing Python just runs the script directly. Either way,
you'll then get an interactive prompt:

```
Please select an image from the following inputs (1, 2, ...):
1. color_blur
2. pelican
3. pixel_rainbow
```

followed by a choice of filter (grayscale, invert, or horizontal flip).
Output is written to `tests/output_cpp/` or `tests/output_python/` depending
on which implementation you ran.

## Verifying output

`tests/output_solutions/` contains precomputed outputs for all three sample
images across all three filters, so you can compare your generated output
against a known-correct result without constructing your own test case or
inspecting anything visually.

## Sample images

Three test images are included in `tests/input/`, chosen to exercise
different parts of the pixel data:

- `color_blur.ppm`
- `pixel_rainbow.ppm`
- `pelican.ppm`

You can test with your own images too. Drop any P3-format `.ppm` file into
`tests/input/` and it will show up in the selection list the next time you
run either implementation.
