Arch API

*POST GET UPDATE DELETE
for{
    Users{
        id
        name
        email
        desciption
        AvatarImg
        group[]
    }
    Folders{
        id__init__
        id__Others__[arr]
        project{
            folder{
                files{
                    docsPDF
                    docsIMG
                    docsTXT
                }
            }
        }
    }
}