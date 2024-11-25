using System.Security.Cryptography.X509Certificates;

namespace TemplateMethod
{
    public abstract class MailParser
    {
        public virtual string ParseMailBody(int identifier)
        {
            return "Parse mail body";
        }

        public virtual void FindServer()
        {
            Console.WriteLine("find server...");
        }

        public virtual void AuthenticateToServer()
        {
            Console.WriteLine("Authenticate to Server...");
        }

        public string ParseHTMLBody(int identifier)
        {
            return "Parse HTML body";
        }
    }

    public class ExchangeMailParser : MailParser
    {
        public override void AuthenticateToServer()
        {
            base.AuthenticateToServer();
            Console.WriteLine("from exchange mail parser");
        }
    }

    public class EudoraMailParser : MailParser
    {
        public override void FindServer()
        {
            Console.WriteLine("find server...");
        }

        public override void AuthenticateToServer()
        {
            base.AuthenticateToServer();
            Console.WriteLine("from eudora mail parser");
        }

    }
}
