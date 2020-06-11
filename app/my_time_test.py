import timeit

mysetup = "from index import process_users"

mycode = "process_users()"

if __name__ == '__main__':
    print(timeit.timeit(stmt=mycode, setup=mysetup, number=100))
