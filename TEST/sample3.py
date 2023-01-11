def main():
    import re

    string = "4K修复如果没人爱我-猫和老鼠四川方言P76-4K_Tom-BV1dS4y1x7d7-RZRJrAXSye6jBZK2"

    match = re.search(r"-\w+$", string)

    if match:
        print(match.group())


if __name__ == '__main__':
    main()
