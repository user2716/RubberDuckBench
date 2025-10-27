import java.util.List;
import java.util.ArrayList;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;


public class NacosRoleServiceImpl {

    private volatile Map<String, List<RoleInfo>> roleInfoMap = new ConcurrentHashMap<>();
    private static final int DEFAULT_PAGE_NO = 1;
    private final String EMPTY = "";

    private RolePersistService rolePersistService;
    private AuthConfigs authConfigs;

    public NacosRoleServiceImpl() {
        rolePersistService = new RolePersistService();
        authConfigs = new AuthConfigs();
        
    }

    public void triggerReload() {
        //this happens every 15 seconds in the nacos project
        reload();
    }

    private void reload() {
        try {
            Page<RoleInfo> roleInfoPage = rolePersistService.getRolesByUserName(EMPTY, DEFAULT_PAGE_NO, Integer.MAX_VALUE);
            if (roleInfoPage == null) {
                return;
            }

            Map<String, List<RoleInfo>> tmpRoleInfoMap = new ConcurrentHashMap<>(16);
            for (RoleInfo roleInfo : roleInfoPage.getPageItems()) {

                if (!tmpRoleInfoMap.containsKey(roleInfo.getUsername())) {
                    tmpRoleInfoMap.put(roleInfo.getUsername(), new ArrayList<>());
                }

                tmpRoleInfoMap.get(roleInfo.getUsername()).add(roleInfo);
            }
            
            roleInfoMap = tmpRoleInfoMap;
        } catch (Exception e) {
            System.out.println("[LOAD-ROLES] load failed " + e);
        }
    }

    public Page<RoleInfo> getRolesFromDatabase(String userName, int pageNo, int pageSize) {
        Page<RoleInfo> roles = rolePersistService.getRolesByUserName(userName, pageNo, pageSize);
        if (roles == null) {
            return new Page<>();
        }
        return roles;
    }

    public List<RoleInfo> getRolesMod(String username) {
        List<RoleInfo> roleInfoList = roleInfoMap.get(username);

        System.out.println("\troleInfoList is null? " + (roleInfoList == null));
        System.out.println("\tusername: " + username);
        System.out.println("\tusername exists in roleInfoMap? " + (roleInfoMap.containsKey(username)));

        //Modification without null check
        if (!authConfigs.isCachingEnabled()) { 
            Page<RoleInfo> roleInfoPage = getRolesFromDatabase(username, DEFAULT_PAGE_NO, Integer.MAX_VALUE);
            if (roleInfoPage != null) {
                roleInfoList = roleInfoPage.getPageItems();
            }
        }
        return roleInfoList;
    }


    public List<RoleInfo> getRoles(String username) {
        List<RoleInfo> roleInfoList = roleInfoMap.get(username);

        System.out.println("\troleInfoList is null? " + (roleInfoList == null));
        System.out.println("\tusername: " + username);
        System.out.println("\tusername exists in roleInfoMap? " + (roleInfoMap.containsKey(username)));


        //Null check in question. Is it needed?
        if (!authConfigs.isCachingEnabled() || roleInfoList == null) { 
            Page<RoleInfo> roleInfoPage = getRolesFromDatabase(username, DEFAULT_PAGE_NO, Integer.MAX_VALUE);
            if (roleInfoPage != null) {
                roleInfoList = roleInfoPage.getPageItems();
            }
        }
        return roleInfoList;
    }

}
