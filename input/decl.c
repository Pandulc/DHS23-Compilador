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

    double resultado = sumarElementos(c + d + e, entero);

    return 0;
}