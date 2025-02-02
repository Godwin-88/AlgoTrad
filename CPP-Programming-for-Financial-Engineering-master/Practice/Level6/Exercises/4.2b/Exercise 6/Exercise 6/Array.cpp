//
//  Array.cpp
//  Exercise 6
//
//  Created by Changheng Chen on 2/2/17.
//  Copyright © 2017 Changheng Chen. All rights reserved.
//

#ifndef Array_cpp
#define Array_cpp

#include "SizeMismatchException.hpp"
#include "OutOfBoundsException.hpp"
#include "Array.hpp"
#include <iostream>

namespace chako
{
    namespace Containers
    {
        // =================================================================
        // Static default size of array
        template <typename T>
        int Array<T>::d_size = 12;
        
        // =================================================================
        // Constructors, destructor, and assignment operator
        template <typename T>
        Array<T>::Array() : m_size(Array<T>::d_size), m_data(new T[Array<T>::d_size])
        { // Default constructor
    
            //cout << "Array default constructor..." << endl;
        }

        template <typename T>
        Array<T>::Array(int size) : m_size(size), m_data(new T[size])
        { // Constructor with size
    
            //cout << "Array constructor with size..." << endl;
        }

        template <typename T>
        Array<T>::Array(const Array<T>& source) : m_size(source.m_size), m_data(new T[source.m_size])
        { // Copy constructor
    
            for (int i = 0; i < m_size; i++)
                m_data[i] = source.m_data[i];
            
            //cout << "Array copy constructor..." << endl;
        }

        template <typename T>
        Array<T>::~Array()
        { // Destructor
    
            delete [] m_data;
            //cout << "By my array..." << endl;
        }

        template <typename T>
        Array<T>& Array<T>::operator = (const Array<T>& source)
        { // Assignment operator
            
            if (this == &source)
                return *this;
    
            delete [] m_data;
            m_size = source.m_size;
            m_data = new T[m_size];

            for (int i = 0; i < m_size; i++)
                m_data[i] = source.m_data[i];
    
            return *this;
        }

        // =================================================================
        // Getter functions
        template <typename T>
        int Array<T>::Size() const
        {
            return m_size;
        }
        
        template <typename T>
        int Array<T>::DefaultSize() const
        {
            return d_size;
        }

        template <typename T>
        T& Array<T>::GetElement(int index) const
        {
            if (index >= m_size || index < 0)
                throw OutOfBoundsException(index);
    
            return m_data[index];
        }

        // Setter function
        template <typename T>
        void Array<T>::DefaultSize(int size)
        {
            d_size = size;
        }
        
        template <typename T>
        void Array<T>::SetElement(int index, const T& p)
        {
            if (index >= m_size || index < 0)
                throw OutOfBoundsException(index);
    
            m_data[index] = p;
        }

        // Operator overloading
        template <typename T>
        T& Array<T>::operator [] (int index)
        {
            if (index >= m_size || index < 0)
                throw OutOfBoundsException(index); 
    
            return m_data[index];
        }
        
        template <typename T>
        const T& Array<T>::operator [] (int index) const
        {
            if (index >= m_size || index < 0)
                throw OutOfBoundsException(index);
            
            return m_data[index];
        }
    }
}

#endif
