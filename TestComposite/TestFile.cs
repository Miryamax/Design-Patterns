using System.Net;
using Xunit;
using FluentAssertions;
using Composite;



namespace TestComposite
{
    public class TestFile
    {
        [Fact]
        public void TestFileSize()
        {
            // Arrange
            long size = 32;
            FileSystemItem file = new Composite.File(size);


            // Act
            long result = file.GetSize();

            // Assert
            result.Should().Be(size);

        }
    }
}