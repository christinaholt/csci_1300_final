! f90 wrapper for the nemsio read module. Given a variable name, level, and
! level type, returns the lat, lon, and slice of the nemsio file.

subroutine get_nemsio_dims(filename, dimx, dimy)

    use nemsio_module

! Inputs
    character(len=500),      intent(in)   :: filename

! Outputs
    integer(nemsio_intkind), intent(out)  :: dimx
    integer(nemsio_intkind), intent(out)  :: dimy

! Local variables
    type(nemsio_gfile)                    :: gfile
    integer(nemsio_intkind)               :: iret

! f2py intent(in) filenme
! f2py intent(out) lat
! f2py intent(out) lon

    iret = 0

! Initialize nemsio file
    call nemsio_init(iret=iret)
    if (iret .ne. 0) then
        write(*,*) "FAILED ON NEMSIO_INIT", iret
        call exit(1)
    endif

! Open the nemsio file for reading
    call nemsio_open(gfile, trim(adjustl(filename)), 'read', iret=iret)
    if (iret .ne. 0) then
        write(*,*) "FAILED ON NEMSIO_OPEN", iret
        call exit(1)
    endif

! Read the dimensions from the file header
    call nemsio_getfilehead(gfile, dimx=dimx, dimy=dimy, iret=iret)
    if (iret .ne. 0) then
        write(*,*) "FAILED ON NEMSIO_GFH", iret
        call exit(1)
    endif

! Close the nemsio file
    call nemsio_close(gfile, iret=iret)
    if (iret .ne. 0) then
        write(*,*) "FAILED ON NEMSIO_CLOSE", iret
        call exit(1)
    endif

end subroutine get_nemsio_dims

subroutine read_nemsio_wrapper(filename, var_name, levtype,  &
                               lev, dimx, dimy,              &
                               lat, lon, var)

    use nemsio_module

! Inputs
    character(len=500),      intent(in)   :: filename
    character(len=500),      intent(in)   :: var_name
    character(len=500),      intent(in)   :: levtype

    integer(nemsio_intkind), intent(in)   :: lev
    integer(nemsio_intkind), intent(in)   :: dimx
    integer(nemsio_intkind), intent(in)   :: dimy

! Outputs
    real(nemsio_intkind), intent(out)   :: lat(dimx,dimy)
    real(nemsio_intkind), intent(out)   :: lon(dimx,dimy)
    real(nemsio_intkind), intent(out)   :: var(dimx,dimy)

! Local variables
    type(nemsio_gfile)                    :: gfile

    real(nemsio_intkind)                 :: data(dimx*dimy)
    real(nemsio_intkind), allocatable    :: tmparr(:)

    integer(nemsio_intkind)               :: iret


    real(nemsio_intkind), allocatable    :: variable(:)

! f2py intent(in) filename
! f2py intent(in) var_name
! f2py intent(in) levtype
! f2py intent(in) lev
! f2py intent(in) dimx
! f2py intent(in) dimy
! f2py intent(out) lat
! f2py intent(out) lon
! f2py intent(out) var
! f2py depend(dimx, dimy) lat
! f2py depend(dimx, dimy) lon
! f2py depend(dimx, dimy) var


! Initialize nemsio file
    call nemsio_init(iret=iret)

! Open the nemsio file for reading
    call nemsio_open(gfile, trim(adjustl(filename)), 'read', iret=iret)

! Allocate, extract,  and reshape the lat/lon values for delivery
    if(.not. allocated(tmparr)) allocate(tmparr(dimx*dimy))

    call nemsio_getfilehead(gfile, lat=tmparr(:))
    lat = reshape(tmparr, (/dimx, dimy/))


    call nemsio_getfilehead(gfile, lon=tmparr(:))
    lon = reshape(tmparr, (/dimx, dimy/))


! Read the field
    call nemsio_readrecv(gfile, trim(adjustl(var_name)),          &
                         levtyp=trim(adjustl(levtype)),           &
                         lev=lev, data=data, iret=iret)

! Reshape the variable to a 2D array
    if(iret == 0 )  then
        var = reshape(data, (/dimx, dimy/))
    else
        write(*,*) "IRET: ", iret
        write(*,*) "Failed to read nemsio field ", trim(adjustl(var_name))
        call exit(1)
    endif

! Deallocate arrays
    if(allocated(tmparr)) deallocate(tmparr)

! Close the nemsio file
    call nemsio_close(gfile, iret=iret)

end subroutine read_nemsio_wrapper
