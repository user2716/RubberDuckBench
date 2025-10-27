public class Main {

    //The Secor Config is set from system properties. There are no guarantees it will be valid.
    public static String getPrefix(SecorConfig config) {
        String prefix = null;
        if (config.getCloudService().equals("Swift")) {
            prefix = "swift://";
        } else if (config.getCloudService().equals("S3")) {
            prefix = "s3://";
        } else if (config.getCloudService().equals("GS")) {
            prefix = "gs://";
        } else if (config.getCloudService().equals("Azure")) {
            prefix = "azure://";
        }
        return prefix;
    }

    public static void main(String[] args) {

        SecorConfig config = new SecorConfig("Swift");
        String prefix = getPrefix(config);
        String topic = "user-events";

        LogFilePath lfp = new LogFilePath(prefix, topic);
        //testing with a non-null prefix
        String out = lfp.getLogFileParentDir();
        System.out.println(out);

        SecorConfig config2 = new SecorConfig("Heroku");
        String prefix2 = getPrefix(config2);

        LogFilePath lfp2 = new LogFilePath(prefix2, topic);
        //testing with a null prefix
        lfp2.getLogFileParentDir();

    }
}
