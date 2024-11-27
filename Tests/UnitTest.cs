using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Singleton;
using Singleton.Interfaces;
using Xunit;
using Moq;



namespace TestSingelton
{
    public class UnitTest
    {
        [Fact]
        public void SingeltonInstanceAreSame()
        {
            //AAA

            // Arrange
            // nothing to arrange this test

            // Act
            ILogger logger1 = Logger.Instance();
            ILogger logger2 = Logger.Instance();


            // Assert

            // compare between the address of the two objects
            Assert.Equal(logger1, logger2);
        }

        [Fact]
        public void WriteMessageToConsole()
        {
            //Arrange
            Mock<ILogger> mockLogger = new Mock<ILogger>();
            string message = "test message by mock";

            //Act
            mockLogger.Object.Log(message);

            //Assert
            mockLogger.Verify(log=> log.Log(It.Is<string>(k => k == "test message by mock")));
        }
    }
}
