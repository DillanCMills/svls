cd external/slang
[ ! -d "build" ] && mkdir build
cd build
/snap/bin/cmake \
   -DCMAKE_CXX_COMPILER=clang++-11 \
   -DCMAKE_BUILD_TYPE=Release \
   -DBUILD_SHARED_LIBS=ON \
	-DSLANG_INCLUDE_TESTS=OFF \
	.. ; 
   # -DCMAKE_INSTALL_PREFIX=/usr/local/bin \
	# -DPython_INCLUDE_DIR= \
	# -DPython_EXECUTABLE= \
	# -DPython_LIBRARY= \
make -j8 ;
cd ../../../
