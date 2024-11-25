using System;
using System.Collections.Generic;
using System.Diagnostics.Metrics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Command
{
    public class Employee
    {
        private static int counter = 0;
        public int Id { get; set; }
        public string Name { get; set; }

        public Employee(string name)
        {
            Id = ++counter;
            Name = name;
        }
    }
}
