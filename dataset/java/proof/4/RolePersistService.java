import java.util.List;
import java.util.ArrayList;

public class RolePersistService {
    List<RoleInfo> roleInfoList;

    public RolePersistService() {
        roleInfoList = new ArrayList<RoleInfo>();

        roleInfoList.add(new RoleInfo("ROLE_ADMIN", "admin"));
        roleInfoList.add(new RoleInfo("ROLE_ADMIN", "sysadmin"));
        roleInfoList.add(new RoleInfo("ROLE_ADMIN", "alice.smith"));
        roleInfoList.add(new RoleInfo("ROLE_USER", "alice.smith"));
        roleInfoList.add(new RoleInfo("ROLE_USER", "bob.smith"));
        roleInfoList.add(new RoleInfo("ROLE_DEVELOPER", "jane.developer"));
        roleInfoList.add(new RoleInfo("ROLE_GUEST", "guest"));
    }

    public Page<RoleInfo> getRolesByUserName(String username, int pageNo, int pageSize) {

        List<RoleInfo> tmpRoleInfoList = new ArrayList<RoleInfo>();

        for (RoleInfo roleInfo : roleInfoList) {
            if (roleInfo.getUsername().equals(username) || username.equals("")) {
                tmpRoleInfoList.add(roleInfo);
            }
        }

        Page p = new Page();
        p.setPageItems(tmpRoleInfoList);

        return p;

    }

}

