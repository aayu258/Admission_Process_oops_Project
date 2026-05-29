class students():
    def __init__(self,name,age,email,contact):
        self.name = name
        self.age = age
        self.email = email
        self.contact = contact
    

    def display_details(self):
        print(self.name)
        print(self.age)
        print(self.email)
        print(self.contact)


class class10Admission(students):
    def __init__(self, name, age, email, contact):
        super().__init__(name, age, email, contact)

        print("admission successful")

class class12Admission(students):
    def __init__(self, name, age, email, contact):
        super().__init__(name, age, email, contact)

        if self.age >= 16:
            print("admission successful")

        else:
            print("admission failed")


print("press 1 for class 10th Admission")
print("press 2 for class 12th Admission")

choice = int(input("Enter your choice:-"))

name = input("Enter your name:-")
age = int(input("Enter your age:-"))
email = input("Enter your email:-")
contact = input("Enter your contact:-")

if choice == 1:
    student1 = class10Admission(name,age,email,contact)
    student1.display_details()

if choice == 2:
    student2 = class12Admission(name,age,email,contact)
    student2.display_details()