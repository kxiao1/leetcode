"""
Automatic differentiation (example from https://en.wikipedia.org/wiki/Automatic_differentiation)
- Forward ('tangent') accumulation
- Reverse ('adjoint') accumulation
"""


# Forward: constructs value and derivative simultaneously. This resembles normal recursion: work 
# is done after the stack is fully expanded. The number of sweeps is the number of variables 
# (e.g. 2 if f = f(x,y)).
class ExpressionForward:
    def __add__(self, other):
        return PlusForward(self, other)

    def __mul__(self, other):
        return MultiplyForward(self, other)


class VariableForward(ExpressionForward):
    def __init__(self, value):
        self.value = value

    def evaluateAndDerive(self, variable):
        partial = 1 if self == variable else 0
        return (self.value, partial)


class PlusForward(ExpressionForward):
    def __init__(self, expressionA, expressionB):
        self.expressionA = expressionA
        self.expressionB = expressionB

    def evaluateAndDerive(self, variable):
        valueA, partialA = self.expressionA.evaluateAndDerive(variable)
        valueB, partialB = self.expressionB.evaluateAndDerive(variable)
        return (valueA + valueB, partialA + partialB)


class MultiplyForward(ExpressionForward):
    def __init__(self, expressionA, expressionB):
        self.expressionA = expressionA
        self.expressionB = expressionB

    def evaluateAndDerive(self, variable):
        valueA, partialA = self.expressionA.evaluateAndDerive(variable)
        valueB, partialB = self.expressionB.evaluateAndDerive(variable)
        return (valueA * valueB, valueB * partialA + valueA * partialB)


# Backward: instead of breaking down the second term of dy/dx = dy/dw1 * dw1/dx, we move the
# operator into the first term and get dy/dx = (dy/dw2 * dw2/dw1) * dw1/dx. Otherwise put, the
# work starts from the top (final function) as in tail recursion. The name could also come from
# the adjoint operator for matrices(the (conjugate) transpose) or the adjoint graph.
# It is in fact the general case of backpropagation in ML: work starts from the objective function
# and gets transformed (e.g. via matrix multiplication back to the inputs)
class ExpressionBackward:
    def __add__(self, other):
        return PlusBackward(self, other)

    def __mul__(self, other):
        return MultiplyBackward(self, other)


class VariableBackward(ExpressionBackward):
    def __init__(self, value):
        self.value = value
        self.partial = 0

    def evaluate(self):
        return self.value

    def derive(self, seed):
        self.partial += seed


class PlusBackward(ExpressionBackward):
    def __init__(self, expressionA, expressionB):
        self.expressionA = expressionA
        self.expressionB = expressionB

    def evaluate(self):
        return self.expressionA.evaluate() + self.expressionB.evaluate()

    def derive(self, seed):
        self.expressionA.derive(seed)
        self.expressionB.derive(seed)


class MultiplyBackward(ExpressionBackward):
    def __init__(self, expressionA, expressionB):
        self.expressionA = expressionA
        self.expressionB = expressionB

    def evaluate(self):
        return self.expressionA.evaluate() * self.expressionB.evaluate()

    def derive(self, seed):
        self.expressionA.derive(self.expressionB.evaluate() * seed)
        self.expressionB.derive(self.expressionA.evaluate() * seed)


# Example: Finding the partials of z = x * (x + y) + y * y at (x, y) = (2, 3)
# Using forward accumulation
x = VariableForward(2)
y = VariableForward(3)
z = x * (x + y) + y * y
value, xPartial = z.evaluateAndDerive(x)
value, yPartial = z.evaluateAndDerive(y)
print("∂z/∂x =", xPartial)  # Output: ∂z/∂x = 7
print("∂z/∂y =", yPartial)  # Output: ∂z/∂y = 8


x = VariableBackward(2)
y = VariableBackward(3)
z = x * (x + y) + y * y
value = z.evaluate()  # we can also cache the value in Plus and Multiply
print("z =", value)  # Output: z = 19
z.derive(1)
print("∂z/∂x =", x.partial)  # Output: ∂z/∂x = 7
print("∂z/∂y =", y.partial)  # Output: ∂z/∂y = 8
