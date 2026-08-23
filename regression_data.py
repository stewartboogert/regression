import json as _json
import shutil as _shutil
from pathlib import Path as _Path
import argparse as _argparse


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

    def to_dict(self):
        d = {
            "name": self.name,
            "file_path": self.file_path,
            "nprimary": self.nprimary,
            "runtime": self.runtime,
            "input_parameters": [p.to_dict() for p in self.input_parameters],
            "output_parameters": [o.to_dict() for o in self.output_parameters],
            "output_files": [o.to_dict() for o in self.output_files]
        }
        return d

    def __repr__(self) -> str:
        s =  f"test_entry(name={self.name}, file_path={self.file_path}, nprimary={self.nprimary}\n"
        s += f"input_parameters={repr(self.input_parameters)}\n"
        s += f"output_parameters={repr(self.output_parameters)}\n"
        s += f"output_files={repr(self.output_files)})"
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


def compare_regression_data(paths : dict,
                            output_path : str = None) -> None :
    '''
    Compare many regression data files
    '''

    # load regression data
    rd_array = [test_entry_store.new_from_json(paths[k]) for k in paths.keys()]

    # verify test_entry_store lengths
    rd_lengths = [len(rd) for rd in rd_array]

    print(rd_lengths)

    # verify same tests are in the store
    for i in range(0, len(rd_array[0])) :
        name0 = rd_array[0][i].name
        for j in range(1, len(rd_array)) :
            if name0 != rd_array[j][i].name :
                print(f"Test {name0} not present in all regression data")

    pass

def html_regression_data(path1 : str = "./regression_data.dat") -> None :
    pass

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
        default="../regression_data/data/os-g4v/",
        metavar="DEST",
        help="Destination directory (default: ../regression_data/data/os-g4v/)"
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

if __name__ == "__main__":
    parser = _build_cli_parser()
    args = parser.parse_args()
    if args.command == "copy":
        copy_regression_data(file_name=args.file, dest_name=args.destination)
