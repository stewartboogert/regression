#!/usr/bin/env python3
import json as _json
import shutil as _shutil
from pathlib import Path as _Path
import argparse as _argparse
import os as _os
from urllib.parse import quote as _urlquote


class test_input_parameter:
    '''
    Class to store test input parameters
    '''
    def __init__(self, name : str, value):
        self.name = name
        self.value = value

    def to_dict(self) -> dict:
        return {"name": self.name, "value": self.value}

    def from_dict(self, d : dict ) -> None:
        self.name = d["name"]
        self.value = d["value"]

    def __repr__(self) -> str:
        return f"test_input_parameter(name={self.name}, value={self.value})"

class test_output_parameter:
    '''
    Class to store test output parameters
    '''

    def __init__(self, name : str, value, rel_tol = 1e-3):
        self.name = name
        self.value = value
        self.rel_tol = rel_tol

    def from_dict(self, d : dict) -> None:
        self.name = d["name"]
        self.value = d["value"]
        self.rel_tol = d["rel_tol"]

    def to_dict(self) -> dict:
        return {"name": self.name, "value": self.value, "rel_tol": self.rel_tol}

    def __repr__(self) -> str:
        return f"test_output_parameter(name={self.name}, value={self.value}, rel_tol={self.rel_tol})"

class test_output_file:
    '''
    Class to store test output files
    '''

    def __init__(self, path : str =None, type : str =None):
        self.path = path
        self.type = type

    def to_dict(self) -> dict:
        return {"path": self.path, "type": self.type}

    def from_dict(self, d : dict) -> None:
        self.path = d["path"]
        self.type = d["type"]

    def __repr__(self):
        return f"test_output_file(path={self.path}, type={self.type})"

class test_entry:
    '''
    Class to store input and output of a single pytest test file
    '''
    def __init__(self,
                 test_name      : str = None,
                 test_file_path : str = None,
                 nprimary       : int = 0,
                 runtime        : float = 0):
        self.name = test_name
        self.file_path = test_file_path
        self.nprimary = nprimary
        self.runtime = runtime
        self.input_parameters = []
        self.output_parameters = []
        self.output_files = []
        self.output_temp_files = []

    def add_input_parameter(self, name : str, value) -> None:
        self.input_parameters.append(test_input_parameter(name, value))

    def add_input_parameter_dict(self, pdict) -> None:
        for k in pdict:
            self.add_input_parameter(k, pdict[k])

    def add_output_parameter(self, name : str, value) -> None:
        self.output_parameters.append(test_output_parameter(name, value))

    def add_output_parameter_dict(self, pdict) -> None:
        for k in pdict:
            self.add_output_parameter(k, pdict[k])

    def add_output_file(self, path : str , type : str) -> None:
        self.output_files.append(test_output_file(path, type))

    def add_output_file_dict(self, fdict) -> None:
        for k in fdict:
            self.add_output_file(k, fdict[k])

    def add_output_temp_file(self, path : str, type : str) -> None:
        self.output_temp_files.append(test_output_file(path, type))

    def add_output_temp_file_dict(self, fdict) -> None:
        for k in fdict:
            self.add_output_temp_file(k, fdict[k])

    def from_dict(self, d) -> None:
        self.name = d["name"]
        self.file_path = d["file_path"]
        self.nprimary = d["nprimary"]
        self.runtime = d["runtime"]
        for v in d["input_parameters"]:
            p = test_input_parameter(None, None)
            p.from_dict(v)
            self.input_parameters.append(p)

        for v in d["output_parameters"]:
            o = test_output_parameter(None, None)
            o.from_dict(v)
            self.output_parameters.append(o)

        for v in d["output_files"]:
            f = test_output_file(None, None)
            f.from_dict(v)
            self.output_files.append(f)

        for v in d["output_temp_files"]:
            f = test_output_file(None, None)
            f.from_dict(v)
            self.output_temp_files.append(f)

    def to_dict(self):
        d = {
            "name": self.name,
            "file_path": self.file_path,
            "nprimary": self.nprimary,
            "runtime": self.runtime,
            "input_parameters": [p.to_dict() for p in self.input_parameters],
            "output_parameters": [o.to_dict() for o in self.output_parameters],
            "output_files": [o.to_dict() for o in self.output_files],
            "output_temp_files": [o.to_dict() for o in self.output_temp_files]
        }
        return d

    def __repr__(self) -> str:
        s =  f"test_entry(name={self.name}, file_path={self.file_path}, nprimary={self.nprimary}\n"
        s += f"input_parameters={repr(self.input_parameters)}\n"
        s += f"output_parameters={repr(self.output_parameters)}\n"
        s += f"output_files={repr(self.output_files)}\n"
        s += f"output_temp_files={repr(self.output_temp_files)})"
        return s

class test_entry_store:
    '''
    Class to store many test_entries (similar API to list)
    '''

    @classmethod
    def new_from_json(cls, file_name):
        s = test_entry_store()
        s.read_json(file_name)
        return s

    def __init__(self):
        self.entries = []

    def new_test_entry(self,
                       test_name : str,
                       test_file_path : str,
                       nprimary : int,
                       runtime : float) -> test_entry:
        te =  test_entry(test_name, test_file_path, nprimary, runtime)
        self.append(te)
        return te

    def append(self, entry : test_entry) -> None:
        self.entries.append(entry)

    def __len__(self) -> int:
        return len(self.entries)

    def __getitem__(self, index : int) -> test_entry:
        return self.entries[index]

    def __setitem__(self, index : int, value) -> None:
        self.entries[index] = value

    def __iter__(self):
        return self.entries.__iter__()

    def write_json(self, file_name : str = "regression_data.dat") -> None:
        with open(file_name, "w") as f:
            f.write("[")
            for i, entry in enumerate(self.entries):
                _json.dump(entry.to_dict(), f)
                if i != len(self.entries)-1 :
                    f.write(",\n")
                else :
                    f.write("\n")
            f.write("]")

    def read_json(self, file_name : str) -> None:
        with open(file_name, "r") as f:
            d = _json.load(f)
            self.from_dict(d)

    def to_dataframe(self):
        pass

    def from_dict(self, d : dict) -> None:
        # loop over entries

        self.entries = []
        for e in d :
            et = test_entry()
            et.from_dict(e)
            self.append(et)

    def __repr__(self) -> str:
        s = "["
        for e in self.entries :
            s += repr(e) + ","

        s += "]"
        return s

def copy_regression_data(file_name : str = "./regression_data.dat",
                         dest_name : str = "./regression_data_store/") -> None :
    '''
    Copy files documented in file_name to destination
    '''

    tes = test_entry_store()
    tes.read_json(file_name)

    # check target path exists
    dest_path = _Path(dest_name)
    if not dest_path.exists():
        dest_path.mkdir(parents=True)

    # copy regressiondata.dat over to target
    _shutil.copy2(file_name, dest_path)

    # loop over files
    tes = test_entry_store.new_from_json(file_name)

    for te in tes :
        test_class = te.name.split('/')[0]
        class_path = _Path(dest_name+'/'+test_class+'/')
        if not class_path.exists():
            class_path.mkdir(parents=True)

        for output in te.output_files :
            output_dest = str(class_path)+'/'+_Path(output.path).parts[-1]
            _shutil.copy2(output.path, output_dest)

def find_entry_in_store(store, name) :
    for e in store :
        if e.name == name :
            return e

def find_input_parameter_in_list(input_parmeters, name) :
    for p in input_parmeters :
        if p.name == name :
            return p

def find_output_parameter_in_list(output_parameters, name) :
    for o in output_parameters :
        if o.name == name :
            return o

def find_output_file_in_list(output_files, name) :
    for o in output_files :
        if o.path == name :
            return o

def compare_input_parameter(input1, input2) :
    pass

def compare_output_parameter(output1, output2) :
    pass

def compare_output_file(files1, files2) :
    pass

def delete_output_files(file_name : str = "./regression_data.dat") -> None:
    '''Delete the files listed in each entry's output_files field.'''
    entries = test_entry_store.new_from_json(file_name)
    for entry in entries:
        for output_file in entry.output_files:
            _Path(output_file.path).unlink(missing_ok=True)


def delete_root_files(path : str) -> None:
    '''Recursively delete all files with a .root suffix under path.'''
    root_path = _Path(path)
    for root_file in root_path.rglob("*.root"):
        if root_file.is_file():
            root_file.unlink()


def compare_regression_data(path1 : str,
                            path2 : str = None) -> None :
    '''
    Compare many regression data files
    '''

    # load test_entry_stores
    store1 = test_entry_store.new_from_json(path1)
    store2 = test_entry_store.new_from_json(path2)

    # loop over entries
    for i, entry1 in enumerate(store1) :
        entry2 = find_entry_in_store(store2, entry1.name)
        if not entry2 :
            continue

        # check if input parameters match
        for j, input1 in enumerate(entry1.input_parameters):
            input2 = find_input_parameter_in_list(entry1.input_parameters, input1.name)
            if not input2 :
                continue

            compare_input_parameter(input1,input2)

        # check if output parameters match
        for j, output1 in enumerate(entry1.output_parameters):
            output2 = find_output_parameter_in_list(entry1.output_parameters, output1.name)
            if not output2 :
                continue
            compare_output_parameter(output1, output2)

        # compare output files
        for j, output_file1, in enumerate(entry1.output_files):
            output_file2 = find_output_file_in_list(entry1.output_files, output_file1.path)
            if not output_file2 :
                continue
            compare_output_file(output_file1, output_file2)


def html_regression_data(path1 : str = "./regression_data.dat",
                        output_path : str = None) -> _Path :
    '''Render a regression-data JSON file as a standalone HTML page.

    Requires the third-party ``dominate`` package.  The generated page is
    written to ``regression_data.html`` alongside the JSON file.
    '''
    import dominate
    from dominate.tags import (
        a, details, h1, li, meta, summary, table, tbody, td, th, thead, tr, ul,
    )

    source = _Path(path1)
    output_path = (
        _Path(output_path)
        if output_path is not None
        else source.with_name("regression_data.html")
    )
    store = test_entry_store.new_from_json(source)
    document = dominate.document(title="Regression tests")

    with document:
        with document.head:
            meta(charset="utf-8")
            meta(name="viewport", content="width=device-width, initial-scale=1")
            # Compact styling keeps the output useful as a standalone file.
            dominate.tags.style(
                dominate.util.raw(
                    "body{font:15px system-ui,sans-serif;margin:2rem;color:#222}"
                    "table{border-collapse:collapse;width:100%}"
                    "th,td{border:1px solid #ccc;padding:.4rem .6rem;"
                    "text-align:left;vertical-align:top}"
                    "th{background:#f2f4f7}"
                    "details{min-width:12rem}"
                    "summary{cursor:pointer;color:#245b8a}"
                    "ul{margin:.4rem 0;padding-left:1.4rem}"
                    "li{margin:.2rem 0;overflow-wrap:anywhere}"
                )
            )

        h1("Regression tests")
        with table():
            with thead():
                with tr():
                    for heading in (
                        "Test", "Test file", "Primary particles", "Runtime (s)",
                        "Input parameters", "Output parameters", "Output files",
                    ):
                        th(heading)
            with tbody():
                for entry in store:
                    with tr():
                        td(entry.name or "Unnamed test")
                        test_file_path = _Path(entry.file_path) if entry.file_path else None
                        test_file = (
                            "/".join(test_file_path.parts[-2:])
                            if test_file_path else ""
                        )
                        if test_file_path:
                            test_file_target = (
                                test_file_path
                                if test_file_path.is_absolute()
                                else source.parent / test_file_path
                            )
                            relative_target = _os.path.relpath(
                                test_file_target,
                                start=output_path.parent,
                            )
                            td(a(test_file, href=_urlquote(relative_target, safe="/")))
                        else:
                            td(test_file)
                        td("" if entry.nprimary is None else str(entry.nprimary))
                        td("" if entry.runtime is None else str(entry.runtime))

                        with td():
                            with details():
                                summary(f"{len(entry.input_parameters)} input parameters")
                                with ul():
                                    for parameter in entry.input_parameters:
                                        li(f"{parameter.name}: {parameter.value}")

                        with td():
                            with details():
                                summary(f"{len(entry.output_parameters)} output parameters")
                                with ul():
                                    for parameter in entry.output_parameters:
                                        li(
                                            f"{parameter.name}: {parameter.value} "
                                            f"(rel_tol={parameter.rel_tol})"
                                        )

                        with td():
                            with details():
                                summary(f"{len(entry.output_files)} output files")
                                with ul():
                                    for output in entry.output_files:
                                        if output.path:
                                            output_name = _Path(output.path).name
                                            test_class = (entry.name or "").split("/")[0]
                                            relative_path = _Path(test_class) / output_name
                                            li(a(output_name, href=relative_path.as_posix()))
                                        else:
                                            li("Unnamed file")

    output_path.write_text(str(document), encoding="utf-8")
    return output_path

def _build_cli_parser() -> _argparse.ArgumentParser:
    parser = _argparse.ArgumentParser(description="Utilities for managing BDSIM regression data")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # copy subcommand
    copy_parser = subparsers.add_parser(
        "copy",
        help="Copy regression data files to a destination directory"
    )
    copy_parser.add_argument(
        "--file",
        default="./regression_data.dat",
        metavar="FILE",
        help="Path to regression data JSON file (default: ./regression_data.dat)"
    )
    copy_parser.add_argument(
        "--destination",
        default="../regression_data/data/html/",
        metavar="DEST",
        help="Destination directory (default: ../regression_data/data/html/)"
    )

    html_parser = subparsers.add_parser(
        "html",
        help="Render a regression-data JSON file as an HTML page"
    )
    html_parser.add_argument(
        "--file",
        default="./regression_data.dat",
        metavar="FILE",
        help="Input regression-data JSON file (default: ./regression_data.dat)"
    )
    html_parser.add_argument(
        "--output",
        default=None,
        metavar="HTML",
        help="Output HTML file (default: regression_data.html beside the input file)"
    )

    # delete subcommand
    delete_parser = subparsers.add_parser(
        "delete",
        help="Delete output files listed in a regression data JSON file"
    )
    delete_parser.add_argument(
        "--file",
        default="./regression_data.dat",
        metavar="FILE",
        help="Path to regression data JSON file (default: ./regression_data.dat)"
    )

    # delete-root subcommand
    delete_root_parser = subparsers.add_parser(
        "delete-root",
        help="Recursively delete .root files under a directory"
    )
    delete_root_parser.add_argument(
        "path",
        metavar="PATH",
        help="Directory to search recursively for .root files"
    )

    return parser

def _parse_key_value(items):
    '''Parse a list of KEY=VALUE strings into a dict'''
    result = {}
    for item in items:
        if "=" not in item:
            raise _argparse.ArgumentTypeError(
                f"Expected KEY=FILE format, got: {item!r}"
            )
        key, _, value = item.partition("=")
        result[key] = value
    return result

def main() -> None:
    """Run the regression-data command line interface."""
    parser = _build_cli_parser()
    args = parser.parse_args()
    if args.command == "copy":
        copy_regression_data(file_name=args.file, dest_name=args.destination)
    elif args.command == "delete":
        delete_output_files(file_name=args.file)
    elif args.command == "delete-root":
        delete_root_files(path=args.path)
    elif args.command == "html":
        output_path = html_regression_data(path1=args.file, output_path=args.output)
        print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
