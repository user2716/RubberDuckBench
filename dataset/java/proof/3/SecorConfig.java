public class SecorConfig {
    //Mock class for a system config
    String cloudService;
    
    public SecorConfig(String service) {
        cloudService = service;
    }

    public String getCloudService() {
        return cloudService;
    }

}
