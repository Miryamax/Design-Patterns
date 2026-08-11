using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection.Metadata.Ecma335;
using System.Text;
using System.Threading.Tasks;
using Iterator.Interfaces;

namespace Iterator
{
    public class PeopleIterator : IPeopleIterator
    {
        private readonly PeopleCollection _PeopleCollection;    
        private int current = 0;
 

        public PeopleIterator(PeopleCollection peopleCollection)
        {
            _PeopleCollection = peopleCollection;
        }

        public Person First()
        {
            current = 0;
            return _PeopleCollection.OrderBy(k => k.Name).First();
        }

        public Person Next()
        {
            current++;
            if (!IsDone())
                return _PeopleCollection
                    .OrderBy(p => p.Name).ElementAt(current);
            return null;
        }

        public bool IsDone()
        {
            return current >= _PeopleCollection.Count;
        }

        Person IPeopleIterator.CurrentItem 
        {
            get
            {
                return _PeopleCollection
                    .OrderBy(p => p.Name).ToList()[current];
            }
        }
    }




    
}
