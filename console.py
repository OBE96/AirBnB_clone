#!/usr/bin/python3
"""Defines the HBnB console."""
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
    curly_brace = re.search(r"\{(.*?)\}", line)
    bracket = re.search(r"\[(.*?)\]", line)
    if curly_brace is None:
        if bracket is None:
            return [i.strip(",") for i in split(line)]
        else:
            lex = split(line[:bracket.span()[0]])
            ret = [i.strip(",") for i in lex]
            ret.append(bracket.group())
            return ret
    else:
        lex = split(line[:curly_brace.span()[0]])
        ret = [i.strip(",") for i in lex]
        ret.append(curly_brace.group())
        return ret


class HBNBCommand(cmd.Cmd):
    """Defines the HolbertonBnB command interpreter.

    Attributes:
        prompt (str): class-level variable that defines the command prompt.
        __classes (dict): class-level variable that is a set containing the
                        names of several classes
    """

    prompt = "(hbnb) "
    valid_classes = {
        "Amenity",
        "BaseModel",
        "City",
        "Place",
        "State",
        "User",
        "Review"
    }

    def __init__(self):
        super().__init__()
        self.arg_dict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }

    def emptyline(self):
        """Do nothing upon receiving an empty line."""
        pass

    def default(self, line):
        """Default behavior for cmd module when input is invalid"""
        match = re.search(r"\.", line)
        if match:
            class_name, command = line.split('.', 1)
            match = re.search(r"\((.*?)\)", command)
            if match:
                command_name, arguments = command.split('(', 1)
                command_name = command_name.strip()
                arguments = arguments.rstrip(')')
                if command_name in self.arg_dict:
                    return self.arg_dict[command_name](f"{class_name} {arguments}")

        print("*** Unknown syntax: {}".format(line))
        return False

    def do_quit(self, line):
        """Quit command to exit the program.\n"""
        print("")
        return True

    def do_EOF(self, line):
        """EOF signal to exit the program."""
        print("")
        return True

    def do_create(self, line):
        """Usage: create <class>
        Create a new class instance and print its id.
        """
        line_list = parse(line)
        if not line_list:
            print("** class name missing **")
            return

        class_name = line_list[0]
        if class_name not in self.valid_classes:
            print("** class doesn't exist **")
            return

        instance = eval(class_name)()
        print(instance.id)
        storage.save()

    def do_show(self, line):
        """Usage: show <class> <id> or <class>.show(<id>)
        Display the string representation of a class instance of a given id.
        """
        line_list = parse(line)
        objdict = storage.all()
        if not line_list:
            print("** class name missing **")
            return
        if line_list[0] not in self.valid_classes:
            print("** class doesn't exist **")
            return
        if len(line_list) < 2:
            print("** instance id missing **")
            return

        obj_key = "{}.{}".format(line_list[0], line_list[1])
        if obj_key not in objdict:
            print("** no instance found **")
            return

        print(objdict[obj_key])

    def do_destroy(self, line):
        """Usage: destroy <class> <id> or <class>.destroy(<id>)
        Delete a class instance of a given id."""
        line_list = parse(line)
        objdict = storage.all()
        if not line_list:
            print("** class name missing **")
            return
        if line_list[0] not in self.valid_classes:
            print("** class doesn't exist **")
            return
        if len(line_list) < 2:
            print("** instance id missing **")
            return

        obj_key = "{}.{}".format(line_list[0], line_list[1])
        if obj_key not in objdict.keys():
            print("** no instance found **")
            return

        del objdict[obj_key]
        storage.save()

    def do_all(self, line):
        """Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects."""
        line_list = parse(line)
        obj_list = []
        objdict = storage.all()

        if line_list and line_list[0] not in self.valid_classes:
            print("** class doesn't exist **")
            return

        for obj in objdict.values():
            if not line_list or line_list[0] == obj.__class__.__name__:
                obj_list.append(obj.__str__())

        print(obj_list)

    def do_count(self, line):
        """Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class."""
        line_list = parse(line)
        count = 0
        objdict = storage.all()

        if not line_list:
            print("** class name missing **")
            return

        if line_list[0] not in self.valid_classes:
            print("** class doesn't exist **")
            return

        for obj in objdict.values():
            if line_list[0] == obj.__class__.__name__:
                count += 1

        print(count)

    def do_update(self, line):
        """Usage: update <class> <id> <attribute_name> <attribute_value> or
           <class>.update(<id>, <attribute_name>, <attribute_value>) or
           <class>.update(<id>, <dictionary>)
            Update a class instance of a given id by adding or updating
            a given attribute key/value pair or dictionary."""
        line_list = parse(line)
        objdict = storage.all()

        if not line_list:
            print("** class name missing **")
            return False

        class_name = line_list[0]
        if class_name not in self.valid_classes:
            print("** class doesn't exist **")
            return False

        if len(line_list) < 2:
            print("** instance id missing **")
            return False

        obj_key = "{}.{}".format(class_name, line_list[1])
        if obj_key not in objdict.keys():
            print("** no instance found **")
            return False

        if len(line_list) < 3:
            print("** attribute name missing **")
            return False

        if len(line_list) < 4:
            print("** value missing **")
            return False

        obj = objdict[obj_key]
        attr_name = line_list[2]
        attr_value = line_list[3]

        # Check if the attribute should be updated using a dictionary
        if len(line_list) == 4 and \
            isinstance(attr_value, str) and \
            attr_value.startswith("{") and \
            attr_value.endswith("}"):
            try:
                attr_value = eval(attr_value)
                if not isinstance(attr_value, dict):
                    raise ValueError("Invalid dictionary format")
            except Exception as e:
                print(f"Error parsing dictionary: {e}")
                return False

        setattr(obj, attr_name, attr_value)
        obj.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
