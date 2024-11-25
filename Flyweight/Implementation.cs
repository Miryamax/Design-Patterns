namespace Flyweight
{
    public interface ICharacter
    {
        void Draw(string fontFamily, int fontSize);
    }

    public class CharacterA : ICharacter
    {
        public void Draw(string fontFamily, int fontSize)
        {
            Console.WriteLine($"A = font family {fontFamily}, font size {fontSize}");
        }
    }

    public class CharacterB : ICharacter
    {
        public void Draw(string fontFamily, int fontSize)
        {
            Console.WriteLine($"B = font family {fontFamily}, font size {fontSize}");
        }
    }

    public class CharacterFactory
    {
        List<ICharacter> storage = new List<ICharacter>();

        public ICharacter GetCharacter(string identifer)
        {
            return new CharacterA();   // for example
        }
    }
}
