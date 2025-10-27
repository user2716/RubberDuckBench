import java.util.Collections;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

public class UIDFetchCommandTest {

    public enum Item {
        FLAGS,
        ENVELOPE,
        STRUCTURE,
        BODY_SANE,
        BODY,
    }

    private IMapMessage createImapMessage(String uid) {
        return new IMapMessage(uid);
    }


    private UidFetchCommand createUidFetchCommand(Long uid, Item... items) {
        FetchProfile fetchProfile = new FetchProfile();
        Collections.addAll(fetchProfile, items);

        return new UidFetchCommand.Builder()
            //Line in question - should the singletonMap be wrapped in a HashMap constructor?
            .messageParams(fetchProfile, new HashMap<>(Collections.singletonMap(String.valueOf(uid),
                            (Message) createImapMessage(String.valueOf(uid)))))
            .build();
    }


    public static void main(String[] args) {
        Long uid = 42L;
        String s_uid = String.valueOf(uid);
        Message msg = new IMapMessage(s_uid);

        Map<String, Message> m = Collections.singletonMap(s_uid, msg);

        Map<String, Message> hm = new HashMap<>(Collections.singletonMap(s_uid, msg));

        
        // Demonstrate the map is immutable
        System.out.println("=============================================== Rubric Item 1: Immutability ==================================");
        try {
            m.put("999", new IMapMessage("999"));
            System.out.println("ERROR: Singleton Map allowed modification!");
        } catch (UnsupportedOperationException e) {
            System.out.println("Singleton Map put() threw UnsupportedOperationException");
        }

        try {
            hm.put("999", new IMapMessage("999"));
            System.out.println("Hash Map allowed put() modification");
        } catch (UnsupportedOperationException e) {
            System.out.println("ERROR: Hash Map Map put() threw UnsupportedOperationException");
        }


        System.out.println("=============================================== Rubric Item 2: Size ==================================");
        System.out.println("Singleton Map size: " + m.size());
        System.out.println("Singleton Map contents: " + m);
        System.out.println();
        System.out.println("Hash Map size: " + hm.size());
        System.out.println("Hash Map contents: " + hm);

    }


}
