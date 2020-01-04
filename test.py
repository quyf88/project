def constellation():
    """第一题：星座分析"""
    print('第一题：星座分析')
    a = input('请输入您的名字:')
    print("""1:水瓶座,2:双鱼座,3:白羊座,4:金牛座,5:双子座,6:巨蟹座,7:狮子座,8:处女座""")
    b = int(input('请根据如上提示输入对应编号:'))
    if b == 1:
        print(a + '您好!您的星座分析结果:1月20-2月18')
    elif b == 2:
        print(a + '您好!您的星座分析结果:2月19-3月20')
    elif b == 3:
        print(a + '您好!您的星座分析结果:3月21-4月19')
    elif b == 4:
        print(a + '您好!您的星座分析结果:4月20-5月20')
    elif b == 5:
        print(a + '您好!您的星座分析结果:5月21-6月21')
    elif b == 6:
        print(a + '您好!您的星座分析结果:6月21-7月22')
    elif b == 7:
        print(a + '您好!您的星座分析结果:7月23-8月22')
    elif b == 8:
        print(a + '您好!您的星座分析结果:8月23-9月22')

    print('*' * 30)


def calculation():
    """第二题：均值 方差 标准差"""
    print('第二题：均值 方差 标准差')
    import numpy
    a = [11, 2, 5]
    # 求均值
    b = numpy.mean(a)
    # 求方差
    c = numpy.var(a)
    # 求标准差
    d = numpy.std(a, ddof=1)
    print("平均值为：%f" %b)
    print("方差为：%f" %c)
    print("标准差为：%f" %d)
    print('*' * 30)


def triangle():
    """第三题：打印等腰三角形"""
    print('第三题：打印等腰三角形')
    for a in range(8):
        for b in range(8 - a - 1):
            print("", end=" ")
        for b in range(2 * a + 1):
            print('*', end='')
        print()
    print('*' * 30)


def rectangle():
    """第四题：打印矩形"""
    print('第四题：打印矩形')
    for a in range(8):
        for b in range(8):
            print("*", end=" ")
        print()


def diamond():
    """第五题： 打印菱形"""
    print('第五题： 打印菱形')
    for a in range(6):
        for b in range(5 - a):
            print(" ", end=" ")
        for b in range(2 * a + 1):
            print("*", end=" ")
        print()
    for a in range(5):
        for b in range(a + 1):
            print(" ", end=" ")
        for c in range((9 - 3 * a) + a):
            print("*", end=" ")
        print()


def multiplication():
    """第六题：打印99乘法表"""
    print('第六题：打印99乘法表')
    for a in range(1, 10):
        for b in range(1, a + 1):
            print("%s*%s=%s" % (b, a, a * b), end=" ")
        print("")


if __name__ == '__main__':
    constellation()
    calculation()
    triangle()
    rectangle()
    diamond()
    multiplication()