import java.util.Collections;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

public class UIDFetchCommandTestMod {

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
            //Line in question - Modified to pass a singletonMap. Should not compile
            .messageParams(fetchProfile, Collections.singletonMap(String.valueOf(uid),
                            (Message) createImapMessage(String.valueOf(uid))))
            .build();
    }


    public static void main(String[] args) {
        

    }


}
