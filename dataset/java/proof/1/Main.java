public class Main {

    public static void testDrawerDisabled() {
        boolean drawerEnabled = false;

        MessageList m = new MessageList(drawerEnabled, 1);
        m.openFolder("inbox");
        System.out.println();

        MessageList m2 = new MessageList(drawerEnabled, 2);
        m2.openFolder("inbox");

    }

    public static void testDrawerEnabled() {
        boolean drawerEnabled = true;

        MessageList m = new MessageList(drawerEnabled, 1);
        m.openFolder("inbox");
        System.out.println();

        MessageList m2 = new MessageList(drawerEnabled, 2);
        m2.openFolder("inbox");

    }


    public static void main(String[] args) {

        System.out.println("Testing with a non-null drawer value to confirm actionBarSubtitle visibility is set: ");
        testDrawerEnabled();
        System.out.println();

        System.out.println("Testing with a null drawer value to confirm actionBarSubtitle visibility is not set: ");
        testDrawerDisabled();
        
        //m.initializeFromLocalSearch(search);

        //1. actionaBarSubtitle.setVisibility does not depend on drawer
        //2. > it has no usages
        //3. actionaBarSubtitle.setVisibility is not called when drawer is null
        //4.  > it is called when drawer is non-null

    }

}
