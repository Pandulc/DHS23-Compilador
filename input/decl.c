int f(int a, int b);

int main()
{
    int x = 10;
    int y = f(x, 12350 * 22);
}

int f(int a, int b)
{
    return a * 2 + b % 5;
}