#ifndef THREE_H
#define THREE_H

#include <map>
#include <string>
#include <vector>

enum ButtonType { UniformEvenButton, UniformButton, CustomButton, LogValueButton };

enum SliceType { UniformEven, Uniform, Custom, LogValue };

struct QRadioButton {
    ButtonType type;
}; //mock

class QtReflEventView {
    public:
        //QtReflEventView();
        void toggleSlicingOptions() const;

        std::string getTimeSlicingType() const;
        std::string getTimeSlicingType2() const;

        QRadioButton* getCheckedButton() const;

    private:
        mutable SliceType m_sliceType;

        std::map<SliceType, std::string> m_sliceTypeStrMap = {
            {SliceType::Uniform, "Uniform"},
            {SliceType::UniformEven, "UniformEven"},
            {SliceType::Custom, "Custom"},
            {SliceType::LogValue, "LogValue"}};


        std::vector<QRadioButton *> m_buttonList = {
            new QRadioButton{UniformEvenButton},
            new QRadioButton{UniformButton},
            new QRadioButton{CustomButton},
            new QRadioButton{LogValueButton} 
        };

        

};

#endif
