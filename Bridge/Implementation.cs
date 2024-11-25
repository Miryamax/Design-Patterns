namespace Bridge
{

    public interface ICoupon
    {
         int CouponValue { get;  }
    }

    public class OneEuroCoupon : ICoupon
    {
        public int CouponValue { get =>1 ; }
    }

    public class TwoEuroCoupon : ICoupon
    {
        public int CouponValue
        {
            get => 2;
        }
    }

    public abstract class Menu
    {
        public abstract int CalculatePrice();
        public readonly ICoupon Coupon = null;

        public Menu(ICoupon _coupon)
        {
            Coupon = _coupon;
        }

    }

    public class VegetarianMenu : Menu
    {
        public VegetarianMenu(ICoupon coupon): base(coupon)
        {}
        public override int CalculatePrice()
        {
            return 100;
        }

    }

    public class MeatBasedMenu : Menu
    {
        public MeatBasedMenu(ICoupon coupon) : base(coupon)
        { }
        public override int CalculatePrice()
        {
            return 200;
        }
    }

}