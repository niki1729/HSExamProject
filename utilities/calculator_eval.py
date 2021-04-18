import math
from math import *


class InputStream:
    def __init__(self, exp):
        self.pos = 0  # position
        self.expres = exp

    def end(self):
        return self.pos >= len(self.expres)

    def next(self):
        self.pos += 1
        return self.expres[self.pos - 1]

    def push_back(self):
        if self.pos > 0:
            self.pos -= 1


class Stack:
    def __init__(self):
        self.list = []

    def push(self, element):
        self.list.append(element)

    def peek(self):
        try:
            return self.list[-1]
        except:
            return None

    def is_empty(self):
        return len(self.list) <= 0

    def pop(self):
        element = self.list[-1]
        del self.list[-1]
        return element


class OpenBracket:
    def to_postfix(self, operation_stack, result):
        operation_stack.push(self)

    def __str__(self):
        return "("


class ClosedBracket:
    def to_postfix(self, operation_stack, result):
        while not operation_stack.is_empty():
            o = operation_stack.pop()
            if not isinstance(o, OpenBracket):
                result.append(o)
            else:
                break


class Number:
    def __init__(self, value):
        self.value = value

    def to_postfix(self, operation_stack, result):
        result.append(self)

    def calculate(self, stack):
        stack.push(self.value)


class Operations:
    def to_postfix(self, operation_stack, result):
        o = operation_stack.peek()
        while o is not None and not isinstance(o, OpenBracket) and o.priority() >= self.priority():
            result.append(o)
            operation_stack.pop()  # remove o from operations_stack
            o = operation_stack.peek()
        operation_stack.push(self)

    def priority(self):
        raise NotImplementedError("Please Implement this method")

    def get_values(self, stack):
        return stack.pop(), stack.pop()


class Plus(Operations):
    def priority(self):
        return 1

    def calculate(self, stack):
        el1, el2 = self.get_values(stack)
        stack.push(el2 + el1)


class Minus(Operations):
    def priority(self):
        return 1

    def calculate(self, stack):
        el1, el2 = self.get_values(stack)
        stack.push(el2 - el1)


class Multiple(Operations):
    def priority(self):
        return 3

    def calculate(self, stack):
        el1, el2 = self.get_values(stack)
        stack.push(el2 * el1)


class Division(Operations):
    def priority(self):
        return 3

    def calculate(self, stack):
        el1, el2 = self.get_values(stack)
        stack.push(el2 / el1)


class UnaryOperations:
    def to_postfix(self, operation_stack, result):
        o = operation_stack.peek()
        while o is not None and not isinstance(o, OpenBracket) and o.priority() > self.priority():
            result.append(o)
            operation_stack.pop()  # remove o from operations_stack
            o = operation_stack.peek()
        operation_stack.push(self)

    def priority(self):
        raise NotImplementedError("Please Implement this method")


class UnaryMinus(UnaryOperations):
    def priority(self):
        return 5

    def calculate(self, stack):
        el = stack.pop()
        stack.push(-el)


class UnaryRoot(UnaryOperations):
    def priority(self):
        return 5

    def calculate(self, stack):
        el = stack.pop()
        stack.push(math.sqrt(el))


class Eval:

    def __init__(self):
        self.exp = ""
        self.exp_tokens = []
        self.l_numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "."]
        self.l_symbols = ["+", "-", "/", "*", "(", ")", "√"]
        self.postfix_list = []

    def evaluate(self, expression):
        self.exp = expression
        # print(expression, "expression")
        self.exp_tokens = self.tokenizer(self.exp)
        print(self.exp_tokens, "parser_exp")

        postfix_form = self.to_postfix_form()
        print(postfix_form)

        return self.calculate(postfix_form)

    def tokenizer(self, exp):
        inp = InputStream(exp)
        tokens = []
        while not inp.end():
            c = inp.next()
            if c in self.l_symbols:
                tokens.append(c)

            if c in self.l_numbers:
                puffer = [c]
                while not inp.end():
                    c = inp.next()
                    if c in self.l_numbers:
                        puffer.append(c)
                    else:
                        inp.push_back()
                        break
                tokens.append("".join(puffer))

        return tokens

    def to_postfix_form(self):
        previous_token = None
        operations_stack = Stack()
        result_l = []
        for i in range(len(self.exp_tokens)):
            token = self.return_object(self.exp_tokens[i], previous_token)
            token.to_postfix(operations_stack, result_l)
            previous_token = token

        while not operations_stack.is_empty():
            o = operations_stack.pop()
            if not isinstance(o, OpenBracket):
                result_l.append(o)
        return result_l

    def return_object(self, element, previous_token):
        if element == "+":
            return Plus()

        if element == "-":
            if self.is_unary_sign(previous_token):
                return UnaryMinus()
            else:
                return Minus()

        if element == "*":
            return Multiple()

        if element == "/":
            return Division()

        if element == "(":
            return OpenBracket()

        if element == ")":
            return ClosedBracket()

        if element == "√":
            return UnaryRoot()

        return Number(float(element))

    def is_unary_sign(self, p_token):
        if isinstance(p_token, Operations) or isinstance(p_token, UnaryOperations) or isinstance(p_token,
                                                                                                 OpenBracket) or p_token is None:
            return True

    def calculate(self, postfix_form):
        result_stack = Stack()
        for element in postfix_form:
            element.calculate(result_stack)

        result = result_stack.pop()
        if not result_stack.is_empty():
            raise Exception("Invalid Expression")
        return result

    def if_int(self, result):
        if int(result) == result:
            return int(result)
        else:
            return result


def print_list(list):
    for element in list:
        print(element, " ", end="")
    print()

# e = Eval()
# print(e.evaluate(expression=input()))
