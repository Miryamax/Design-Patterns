using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Xunit;
using FluentAssertions;
using Composite;
using Directory = Composite.Directory;

namespace TestComposite
{
    public class TestDirectory
    {
        [Fact]
        public void TestDirectorySize()
        {
            // Arrange
            Directory dir = new Directory();
            for (int i = 1; i <= 10; i++)
                dir._items.Add(new Composite.File(i));
            

            // Act
            long sizeDir = dir.GetSize();

            // Assert
            sizeDir.Should().Be(55);
        }
    }
}
