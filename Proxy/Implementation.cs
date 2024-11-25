namespace Proxy
{
    // the interface that connect between

    public interface IDocument
    {
        void DisplayDocument();
    }


    //real subject
    public class Document : IDocument
    {
        public string Title { get; private set; }

        public string Body { get; private set; }

        public int AuthorId { get; private set; }

        public void LoadDocument()
        {
            Console.WriteLine("load document...");
        }

        public void DisplayDocument()
        {
            Console.WriteLine("display document from the real subject");
        }
    }

    // proxy subject 
    public class DocumentProxy : IDocument
    {
        private Document _document = new Document();
        public void DisplayDocument()
        {
            _document.LoadDocument();
            Console.WriteLine("display document from the proxy subject");
        }
    }
}
