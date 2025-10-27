#include "3.h"
#include <cstdlib>
#include <ctime>
#include <iostream>


QRadioButton* QtReflEventView::getCheckedButton() const {
    return m_buttonList[rand() % 4];
}

void QtReflEventView::toggleSlicingOptions() const {

    const QRadioButton* checkedButton = QtReflEventView::getCheckedButton();

    SliceType slicingTypes[4] = {SliceType::UniformEven, SliceType::Uniform,
        SliceType::Custom, SliceType::LogValue};

    for (size_t i = 0; i < m_buttonList.size(); i++) {
        if (m_buttonList[i] == checkedButton) {
            m_sliceType = slicingTypes[i]; //m_sliceType is set to be 1 of 4 SliceTypes.
            break;
        }
    }
}

/** Returns the type of time slicing that was selected as string
 * @return :: Time slicing type
 */
std::string QtReflEventView::getTimeSlicingType() const {
    return m_sliceTypeStrMap.at(m_sliceType); //line number question in the PR
    //    return m_sliceTypeStrMap[m_sliceType]; //operator[] causes compiler error due to const
}

int main() {
    srand(time(0));

    QtReflEventView view;

    view.toggleSlicingOptions(); //set m_sliceType
    std::cout << view.getTimeSlicingType() << std::endl; //m_sliceType will always be present in the map, based on the map initialization and assignments of m_sliceType

    
    //1. discuss how each operation handles non-existent keys? [2]
    // The answer should state that the at function throws an exception when the key does not exist. 1 point should be deducted if this is not mentioned 
    //The answer should state that the [] operator inserts a new element with the non-existent key. 1 point should be deducted if this is not mentioned 


    //2. Does the answer discuss how each operation can be used in the context of a const method? [2] 
    //The answer should mention or imply that the method is marked as const. 1 point should be deducted if this is not mentioned. 
    //The answer should explain that [] cannot be called in a const method. 1 point should be deducted if this is not mentioned. 
}
