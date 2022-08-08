#!/usr/bin/python3
""" A Command Line Interpreter using the built-in cmd module.

The class HBNBCommand inherits from the cmd.Cmd class which allows us to
make us of the methods and attributes associted with the cmd.Cmd class

"""
import cmd
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models import storage


class HBNBCommand(cmd.Cmd):
    """ Defines attributes(method and fields) for Command Interpreter Class.

    Attributes:
        intro (str): An introduction to the CLI
        prompt (str): A prompt which takes in commands
    """
    prompt = "(hbnb) "

    class_list = ["BaseModel", "User", "State", "City", "Amenity", "Place",
                  "Review"]

    def do_quit(self, args):
        """ Quit command to exit the program

        Args:
            args (str): Arguments passed
        """
        if not args:
            return True
        else:
            print(f"*** Unknowm syntax: quit {args}")

    def do_EOF(self, args):
        """ Indicates end of file. Quits the program

        Args:
            args (str): Arguments passed
        """
        if not args:
            return True
        else:
            print(f"*** Unknown syntax: EOF {args}")

    def emptyline(self):
        """ Do nothing """
        pass

    def do_create(self, args):
        """ Creates a new instance of BaseModel.

        Args:
            args (...): Name of Model passed
        """
        if not args:
            print("** class name missing **")
        else:
            args = args.split()
            if args[0] not in self.class_list:
                print("** class doesn't exist **")
            else:
                new_instance = eval("{}()".format(args[0]))
                print(new_instance.id)
                new_instance.save()

    def do_show(self, args):
        """
        Print string representation of an instance based on classname and id

        Args:
            args (...): Name and id of Model passed
        """
        if not args:
            print("** class name missing **")
        else:
            args = args.split()
            if args[0] not in self.class_list:
                print("** class doesn't exist **")
            elif len(args) < 2:
                print("** instance id missing **")
            else:
                all_instances = storage.all()
                class_instance = args[0] + '.' + args[1]
                if class_instance not in all_instances:
                    print("** no instance found **")
                else:
                    print(all_instances[class_instance])

    def do_destroy(self, args):
        """ Destroy an instance based on className and id

        Args:
            args (...): Name and id of Model Passed
        """
        if not args:
            print("** class name missing **")
        else:
            args = args.split()
            if args[0] not in self.class_list:
                print("** class doesn't exist **")
            elif len(args) < 2:
                print("** instance id missing **")
            else:
                all_instances = storage.all()
                class_instance = args[0] + '.' + args[1]
                if class_instance not in all_instances:
                    print("** no instance found **")
                else:
                    del all_instances[class_instance]
                    storage.save()

    def do_all(self, args):
        """
        Prints all string representation of all instances
        based or not on the class name

        Args:
            args (...): Name of Model passed
        """
        all_instances = storage.all()
        str_list = []
        if len(args) == 0:
            for instance in all_instances:
                str_list.append(str(all_instances[instance]))
            print(str_list)
        else:
            class_instance = args.split()[0]
            if args not in self.class_list:
                print("** class doesn't exist **")
            else:
                for instance in all_instances:
                    if args == instance.split('.')[0]:
                        str_list.append(str(all_instances[instance]))
                print(str_list)

    def do_update(self, args):
        """
        Update an instance based on class name and id
        by adding or updating attribute

        Args:
            args (...): Name, id and atributes of a model
        """

        if not args:
            print("** class name missing **")
        else:
            args = args.split()
            if args[0] not in self.class_list:
                print("** class doesn't exist **")
            elif len(args) < 2:
                print("** instance id missing **")
            else:
                all_instances = storage.all()
                class_instance = args[0] + '.' + args[1]
                if class_instance not in all_instances:
                    print("** no instance found **")
                elif len(args) < 3:
                    print("** attribute name missing **")
                elif len(args) < 4:
                    print("** value missing **")
                else:
                    attr = args[2]
                    value = args[3].strip('"')
                    if hasattr(all_instances[class_instance], attr):
                        attr_type = type(getattr(all_instances[class_instance],
                                         attr))
                        if attr_type == int:
                            setattr(all_instances[class_instance],
                                    attr, int(value))
                        elif attr_type == float:
                            setattr(all_instances[class_instance],
                                    attr, float(value))
                        elif attr_type == str:
                            setattr(all_instances[class_instance],
                                    attr, value)
                        storage.save()
                    else:
                        setattr(all_instances[class_instance], attr, value)
                        storage.save()

    def default(self, args):
        """ Methods with User.

        Args:
            args (str): Arguments passed
        """
        args_list = args.split('.')
        if args_list[0] not in self.class_list or len(args_list) != 2:
            super().default(args)
        else:
            if args_list[1] == "all()":
                self.all_method(args_list[0])
            elif args_list[1] == "count()":
                print(self.count_method(args_list[0]))
            elif args_list[1][:4] == "show":
                tmp = args_list[1].split('"')
                self.do_show(args_list[0] + ' ' + tmp[1])
            elif args_list[1][:7] == "destroy":
                tmp = args_list[1].split('"')
                self.do_destroy(args_list[0] + ' ' + tmp[1])
            elif args_list[1][:6] == "update":
                print("here")

    @classmethod
    def all_method(cls, class_name):
        """ Print all instances 'class name' """
        all_instances = storage.all()
        number = cls.count_method(class_name)
        count = 0
        print("[", end='')
        for key in all_instances:
            if class_name == key.split('.')[0]:
                print(all_instances[key], end='')
                if count != number - 1:
                    print(", ", end='')
                    count += 1
        print("]")

    @staticmethod
    def count_method(class_name):
        """ Print the number of instances of a class """
        all_instances = storage.all()
        count = 0
        for key in all_instances:
            if class_name == key.split('.')[0]:
                count += 1
        return count


if __name__ == '__main__':
    HBNBCommand().cmdloop()
