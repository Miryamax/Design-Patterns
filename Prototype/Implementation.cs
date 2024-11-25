namespace Prototype
{
    // the prototype class
    public abstract class Person
    {
        public abstract Person Clone();

    }

    public class Employee : Person
    {
        public override Person Clone()
        {
            return (Person)MemberwiseClone();
        }
    }

    public class Manager : Person
    {
        public override Person Clone()
        {
            return (Person)MemberwiseClone();
        }
    }

    public class Client
    {
        private Person _person;

        public Client(Person person)
        {
            _person = person.Clone();
        }
    }
}
