double sumarElementos(int a, double b)
{
    double result = a + b;

    return result;
}

int main()
{

    int entero = 5, c, d;

    c = entero;

    d = c;

    int e = d + entero + c;

    double resultado = sumarElementos(c + d + e, 3.14 * 5 + 200 - 12 % 6 + 4 / 8);

    return 0;
}