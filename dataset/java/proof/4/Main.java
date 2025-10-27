import java.util.List;

public class Main {

    public static void testMod(NacosRoleServiceImpl service, String username) {
        System.out.println();
        System.out.println("Calling getRoles WITHOUT the null check for roleInfoList");
        List<RoleInfo> roles = service.getRolesMod(username);

        System.out.println("Returned roles: " + roles);
        System.out.println();
        System.out.println();
        System.out.println("Without the null check for roleInfoList, the code does not query the database and returns null: " + (roles == null));
    }


    public static void test(NacosRoleServiceImpl service, String username) {
        System.out.println();
        System.out.println("Calling getRoles with the null check for roleInfoList");

        List<RoleInfo> roles = service.getRoles(username);

        System.out.println("Returned roles: " + roles);
        System.out.println();
        
    }

    public static void main(String[] args) {
        //roleInfoList can be null if 1. username is not in the map or 2. if the value is null

        System.out.println("============================================================================");
        System.out.println("Testing with invalid username: test");
        System.out.println("============================================================================");

        String username = "test";
        
        System.out.println();
        System.out.println("Testing under situation where roleInfoMap has not been filled yet (no reload triggered)");
        System.out.println("------------------------------------------------------------------------------");


        
        NacosRoleServiceImpl service = new NacosRoleServiceImpl();
        test(service, username);
        testMod(service, username);
        
        System.out.println();

        System.out.println("------------------------------------------------------------------------------");
        System.out.println("Testing case where roleInfoMap has been filled through reload");
        System.out.println("------------------------------------------------------------------------------");
        
        service = new NacosRoleServiceImpl();
        service.triggerReload();

        test(service, username);
        testMod(service, username);


        System.out.println("============================================================================");
        System.out.println("Testing with valid username: alice.smith");
        System.out.println("============================================================================");

        username = "alice.smith";
        
        System.out.println();
        System.out.println("Testing under situation where roleInfoMap has not been filled yet (no reload triggered)");
        System.out.println("------------------------------------------------------------------------------");

        
        service = new NacosRoleServiceImpl();
        test(service, username);
        testMod(service, username);
        
        System.out.println();

        System.out.println("------------------------------------------------------------------------------");
        System.out.println("Testing case where roleInfoMap has been filled through reload");
        System.out.println("------------------------------------------------------------------------------");
        
        service = new NacosRoleServiceImpl();
        service.triggerReload();

        test(service, username);
        testMod(service, username);

        //2. Experiment with different values of cachingEnabled?
        System.setProperty("nacos.core.auth.caching.enabled", "false");
        
        System.out.println();
        System.out.println();
        System.out.println("********************* TESTING AGIAN WITH CACHING DISABLED ******************");
        System.out.println();
        System.out.println("\tWith caching disabled, the null check doesn't have an effect");
        System.out.println();
        System.out.println();


        System.out.println("============================================================================");
        System.out.println("Testing with invalid username: test");
        System.out.println("============================================================================");

        username = "test";
        
        System.out.println();
        System.out.println("Testing under situation where roleInfoMap has not been filled yet (no reload triggered)");
        System.out.println("------------------------------------------------------------------------------");


        
        service = new NacosRoleServiceImpl();
        test(service, username);
        testMod(service, username);
        
        System.out.println();

        System.out.println("------------------------------------------------------------------------------");
        System.out.println("Testing case where roleInfoMap has been filled through reload");
        System.out.println("------------------------------------------------------------------------------");
        
        service = new NacosRoleServiceImpl();
        service.triggerReload();

        test(service, username);
        testMod(service, username);


        System.out.println("============================================================================");
        System.out.println("Testing with valid username: alice.smith");
        System.out.println("============================================================================");

        username = "alice.smith";
        
        System.out.println();
        System.out.println("Testing under situation where roleInfoMap has not been filled yet (no reload triggered)");
        System.out.println("------------------------------------------------------------------------------");

        
        service = new NacosRoleServiceImpl();
        test(service, username);
        testMod(service, username);
        
        System.out.println();

        System.out.println("------------------------------------------------------------------------------");
        System.out.println("Testing case where roleInfoMap has been filled through reload");
        System.out.println("------------------------------------------------------------------------------");
        
        service = new NacosRoleServiceImpl();
        service.triggerReload();

        test(service, username);
        testMod(service, username);

    }
}
