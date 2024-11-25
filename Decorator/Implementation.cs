namespace Decorator
{

    public interface IMailService
    {
        void SendMail();
    }

    public class OnPremiseMailService : IMailService
    {
        public void SendMail()
        {
            Console.WriteLine("send mail on premise...");
        }
    }

    public class CloudMailService : IMailService
    {
        public void SendMail()
        {
            Console.WriteLine("send mail on cloud...");
        }
    }

    public abstract class MailServiceDecoratorBase : IMailService
    {
        private readonly IMailService _mailService;

        public MailServiceDecoratorBase(IMailService mailService)
        {
            _mailService = mailService;
        }

        public virtual void SendMail()
        {
            _mailService.SendMail();
        }
    }

    public class StatisticDecorator : MailServiceDecoratorBase
    {
        public StatisticDecorator(IMailService mailService) : base(mailService)
        {
        }

        public override void SendMail()
        {
            base.SendMail();
            Console.WriteLine("statistic decorator....");
        }
    }

    public class MessageDataBaseDecorator : MailServiceDecoratorBase
    {
        public MessageDataBaseDecorator(IMailService mailService) : base(mailService)
        {
        }

        public override void SendMail()
        {
            base.SendMail();
            Console.WriteLine("statistic decorator....");
        }
    }


}
