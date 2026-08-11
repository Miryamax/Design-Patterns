using Iterator;
using Xunit;
using FluentAssertions;
using Iterator.Interfaces;


namespace TestIterator
{
    public class TestPeopleIterator
    {
        [Fact]
        public void FirstFunctionReturnFirstPerson()
        {
            // Arrange
            PeopleCollection people = new PeopleCollection();
            Person p = new Person("Miryam", "Israel");
            people.Add(p);
            people.Add(new Person("Zuriel", "Israel"));

            // Act
            IPeopleIterator iterator = people.CreateIterator();
            Person person = iterator.First();

            // Assert
            person.Should().Be(p);
        }

        [Fact]
        public void NextFunctionReturnCorrectPerson()
        {
            // Arrange
            PeopleCollection people = new PeopleCollection();
            Person p1 = new Person("Josef", "USA");
            Person p2 = new Person("Rivka", "Israel");
            people.Add(p1);
            people.Add(p2);

            // Act
            IPeopleIterator it = people.CreateIterator();
            Person person = it.Next();

            // Assert
            person.Should().Be(p2);

        }

        [Fact]
        public void NextFunctionReturnNull()
        {
            // Arrange
            PeopleCollection people = new PeopleCollection();
            Person p1 = new Person("Josef", "USA");
            people.Add(p1);

            // Act
            IPeopleIterator it = people.CreateIterator();
            Person person = it.Next();

            // Assert
            person.Should().BeNull();

        }

        [Theory]
        [InlineData(0, "Batya", "Israel", "Miryam", "USA")]
        [InlineData(2, "Michael", "Israel", "Jekob", "Usa")]
        public void CurrentItemIsTheCurrent(int index, string name1, string country1, string name2, string country2)
        {
            // Arrange
            PeopleCollection people = new PeopleCollection();
            Person p1 = new Person(name1, country1);
            people.Add(p1);
            Person p2 = new Person(name2, country2);
            people.Add(p2);

            // Act
            IPeopleIterator iterator = people.CreateIterator();
            Person person = null;


            for (int i = 0; i <= index; i++)
                person = iterator.Next();
            

            // Assert
            if (index >= 2)
                person.Should().BeNull();
            else
            {
               

                person = index == 0 ? p2 : p1;
                person.Should().Be(person);

            }
            

        }

    }

}