#!/usr/bin/python3
"""HBnB console."""
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def parse(line):
    cur_brace = re.search(r"\{(.*?)\}", line)
    bracket = re.search(r"\[(.*?)\]", line)
    if cur_brace is None:
        if bracket is None:
            return [j.strip(",") for j in split(line)]
        else:
            lex = split(line[:bracket.span()[0]])
            ret = [j.strip(",") for j in lex]
            ret.append(bracket.group())
            return ret
    else:
        lex = split(line[:cur_brace.span()[0]])
        ret = [j.strip(",") for j in lex]
        ret.append(cur_brace.group())
        return ret


class HBNBCommand(cmd.Cmd):
    """HBNB command interpreter.

    Attributes:
        prompt (str): class-level variable that defines the command prompt.
        __cls (dict): class-level variable that containing the names of several
                        classes
    """

    prompt = "(hbnb) "
    __cls = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def emptyline(self):
        """Do nothing upon receiving an empty line."""
        pass

    def default(self, line):
        """Default behavior for cmd module when input is invalid"""
        arg_dt = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        result = re.search(r"\.", line)
        if result is not None:
            line_lt = [line[:result.span()[0]], line[result.span()[1]:]]
            result = re.search(r"\((.*?)\)", line_lt[1])
            if result is not None:
                cmmd = [line_lt[1][:result.span()[0]], result.group()[1:-1]]
                if cmmd[0] in arg_dt.keys():
                    call = "{} {}".format(line_lt[0], cmmd[1])
                    return arg_dt[cmmd[0]](call)
        print("*** Unknown syntax: {}".format(line))
        return False

    def do_quit(self, line):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, line):
        """EOF signal to exit the program."""
        print("")
        return True

    def do_create(self, line):
        """Usage: create <class>
        Create a new class instance and print its id.
        """
        line_lt = parse(line)
        if len(line_lt) == 0:
            print("** class name missing **")
        elif line_lt[0] not in HBNBCommand.__cls:
            print("** class doesn't exist **")
        else:
            print(eval(line_lt[0])().id)
            storage.save()

    def do_show(self, line):
        """Usage: show <class> <id> or <class>.show(<id>)
        Display the string representation of a class instance of a given id.
        """
        line_lt = parse(line)
        obj_dt = storage.all()
        if len(line_lt) == 0:
            print("** class name missing **")
        elif line_lt[0] not in HBNBCommand.__cls:
            print("** class doesn't exist **")
        elif len(line_lt) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(line_lt[0], line_lt[1]) not in obj_dt:
            print("** no instance found **")
        else:
            print(obj_dt["{}.{}".format(line_lt[0], line_lt[1])])

    def do_destroy(self, line):
        """Usage: destroy <class> <id> or <class>.destroy(<id>)
        Delete a class instance of a given id."""
        line_lt = parse(line)
        obj_dt = storage.all()
        if len(line_lt) == 0:
            print("** class name missing **")
        elif line_lt[0] not in HBNBCommand.__cls:
            print("** class doesn't exist **")
        elif len(line_lt) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(line_lt[0], line_lt[1]) not in obj_dt.keys():
            print("** no instance found **")
        else:
            del obj_dt["{}.{}".format(line_lt[0], line_lt[1])]
            storage.save()

    def do_all(self, line):
        """Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects."""
        line_lt = parse(line)
        if len(line_lt) > 0 and line_lt[0] not in HBNBCommand.__cls:
            print("** class doesn't exist **")
        else:
            obj_lt = []
            for obj in storage.all().values():
                if len(line_lt) > 0 and line_lt[0] == obj.__class__.__name__:
                    obj_lt.append(obj.__str__())
                elif len(line_lt) == 0:
                    obj_lt.append(obj.__str__())
            print(obj_lt)

    def do_count(self, line):
        """Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class."""
        line_lt = parse(line)
        cnt = 0
        for obj in storage.all().values():
            if line_lt[0] == obj.__class__.__name__:
                cnt += 1
        print(cnt)

    def do_update(self, line):
        """Usage: update <class> <id> <attribute_name> <attribute_value> or
       <class>.update(<id>, <attribute_name>, <attribute_value>) or
       <class>.update(<id>, <dictionary>)
        Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary."""
        line_lt = parse(line)
        obj_dt = storage.all()

        if len(line_lt) == 0:
            print("** class name missing **")
            return False
        if line_lt[0] not in HBNBCommand.__cls:
            print("** class doesn't exist **")
            return False
        if len(line_lt) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(line_lt[0], line_lt[1]) not in obj_dt.keys():
            print("** no instance found **")
            return False
        if len(line_lt) == 2:
            print("** attribute name missing **")
            return False
        if len(line_lt) == 3:
            try:
                type(eval(line_lt[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(line_lt) == 4:
            obj = obj_dt["{}.{}".format(line_lt[0], line_lt[1])]
            if line_lt[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[line_lt[2]])
                obj.__dict__[line_lt[2]] = valtype(line_lt[3])
            else:
                obj.__dict__[line_lt[2]] = line_lt[3]
        elif type(eval(line_lt[2])) == dict:
            obj = obj_dt["{}.{}".format(line_lt[0], line_lt[1])]
            for q, r in eval(line_lt[2]).items():
                if (q in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[q]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[q])
                    obj.__dict__[q] = valtype(r)
                else:
                    obj.__dict__[q] = r
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
