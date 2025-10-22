from autocomplete import OptimizedAutoCompleteSystem

def main():
    print("Welcome to autocomplete system")
    system = OptimizedAutoCompleteSystem(k=3)
    system.insert("apple", 5)
    system.insert("app", 3) 
    system.insert("application", 8)
    system.insert("appetite", 10)

    print(system.get_suggestions("app"))

if __name__ == '__main__':
    main()
