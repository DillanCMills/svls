cd external/slang
mkdir build && cd build
cmake \
   -DCMAKE_CXX_COMPILER=g++ \
   -DCMAKE_BUILD_TYPE=Release \
   -DCMAKE_INSTALL_PREFIX=/usr/local/bin \
   -DBUILD_SHARED_LIBS=ON \
	-DSLANG_INCLUDE_TESTS=OFF \
	# -DPython_INCLUDE_DIR= \
	# -DPython_EXECUTABLE= \
	# -DPython_LIBRARY= \
	.. ; 
make -j8 ;
