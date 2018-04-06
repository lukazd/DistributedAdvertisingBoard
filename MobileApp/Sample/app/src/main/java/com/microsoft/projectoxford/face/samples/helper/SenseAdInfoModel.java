package com.microsoft.projectoxford.face.samples.helper;

import java.util.Map;

public class SenseAdInfoModel{
    private String sex;
    private String bday;
    private String faceGroupName;
    private String iotaCode;
    private String personName;
    private String personId;
    private Map<String, Float> adPrefs;

    public SenseAdInfoModel(String sex, String bday, String faceGroupName, String personName, String personId, Map<String, Float> adPrefs) {
        this.sex = sex;
        this.bday = bday;
        this.faceGroupName = faceGroupName;
        this.personName = personName;
        this.personId = personId;
        this.adPrefs = adPrefs;
    }


    public String getSex() {
        return sex;
    }

    public void setSex(String sex) {
        this.sex = sex;
    }

    public String getBday() {
        return bday;
    }

    public void setBday(String bday) {
        this.bday = bday;
    }

    public String getFaceGroupName() {
        return faceGroupName;
    }

    public void setFaceGroupName(String faceGroupName) {
        this.faceGroupName = faceGroupName;
    }

    public String getIotaCode() {
        return iotaCode;
    }

    public void setIotaCode(String iotaCode) {
        this.iotaCode = iotaCode;
    }

    public String getPersonName() {
        return personName;
    }

    public void setPersonName(String personName) {
        this.personName = personName;
    }

    public String getPersonId() {
        return personId;
    }

    public void setPersonId(String personId) {
        this.personId = personId;
    }

    public Map<String, Float> getAdPrefs() {
        return adPrefs;
    }

    public void setAdPrefs(Map<String, Float> adPrefs) {
        this.adPrefs = adPrefs;
    }
}