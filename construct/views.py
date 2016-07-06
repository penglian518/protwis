from django.shortcuts import render
from django.views.generic import TemplateView, View

from construct.models import *
from protein.models import Protein, ProteinConformation
from mutation.models import Mutation

from datetime import datetime


# Create your views here.
def detail(request, slug):

    # get constructs
    c = Construct.objects.get(name=slug)

    annotations = {}
    n_term = {}
    insert = {}
    deletion = {}
    pair_no = 0
    for mod in c.modifications.all():
        if mod.position_type == 'pair':
            pair_no += 1
            pair_info = "<br>Pair No"+str(pair_no)+"<br>Between "+str(mod.pos_start)+" - "+str(mod.pos_end)
            pair_short = str(pair_no)
        else:
            pair_info = ''
            pair_short = ''

        annotations[mod.pos_start] = ['mod','modification','Modified<br>'+mod.modification+pair_info,mod,pair_short]
        annotations[mod.pos_end] = ['mod','modification','Modified<br>'+mod.modification+pair_info,mod,pair_short]

    for mut in c.mutations.all():
        annotations[mut.sequence_number] = ['mut','mutation','Mutated from '+mut.wild_type_amino_acid+' to '+mut.mutated_amino_acid,mut]

    for aux in c.insertions.all():
        if aux.start:
            for i in range(aux.start,aux.end+1):
                annotations[i] = [aux.insert_type.name,'Insertion<br>Protein_type: '+aux.insert_type.name,aux]
                insert[aux.start] = aux
        if aux.position.startswith('N-term'):
            n_term[aux.position] = aux

    for dele in c.deletions.all():
        deletion[dele.start] = ['del','deletion','Deleted from '+str(dele.start)+' to '+str(dele.end),dele]
        deletion[dele.end] = ['del','deletion','Deleted from '+str(dele.start)+' to '+str(dele.end),dele]
        for i in range(dele.start,dele.end+1):
            annotations[i] = ['del','deletion','Deleted from '+str(dele.start)+' to '+str(dele.end),dele]

    # get residues
    residues = Residue.objects.filter(protein_conformation__protein=c.protein).order_by('sequence_number').prefetch_related(
        'protein_segment', 'generic_number', 'display_generic_number')

    residues_custom = []
    residues_lookup = {}
    for r in residues:
        residues_lookup[r.sequence_number] = r
        r.print_amino_acid = r.amino_acid
        if r.sequence_number in annotations:
            if annotations[r.sequence_number][1] == 'deletion':
                continue
            if annotations[r.sequence_number][1] == 'insertion':
                continue
            if annotations[r.sequence_number][1] == 'mutation':
                r.print_amino_acid = annotations[r.sequence_number][3].mutated_amino_acid
        residues_custom.append(r)


    chunk_size = 10
    r_chunks_schematic = []
    r_chunks_schematic_construct = []
    r_buffer = []
    a_buffer = []
    last_segment = False
    border = False
    title_cell_skip = 0
    ii = 0
    # create schemtics with annotations
    for i, r in enumerate(residues):
        if (r.protein_segment.slug != last_segment and i!=0) or i == len(residues)-1:
            a_list = {}
            if ii<20:
                counter = ii
                width = 42/(ii+1)
            else:
                counter = 20
                width = 2
            for a in a_buffer:
                temp = a[0]*counter // (ii)
                a_list[temp]  = a[1]
            if (last_segment):
                for a in range(counter+1):
                    if a<len(prev_r.protein_segment.slug):
                        title_cell_skip = 1
                    else:
                        title_cell_skip = 0

                    if a in a_list:
                        annotation = a_list[a]
                    else:
                        annotation = ''

                    if a==0:
                        r_buffer.append([prev_r, True, 0,annotation,width])
                    else:
                        r_buffer.append([prev_r, False, 0,annotation,width])

                r_chunks_schematic.append(r_buffer)
                print(last_segment,counter,len(r_buffer),width,len(r_buffer)*width)
            border = True
            r_buffer = []
            a_buffer = []
            ii = 0

        if r.sequence_number in annotations:
            a_buffer.append([ii,annotations[r.sequence_number]])
        prev_r = r
        last_segment = r.protein_segment.slug
        ii+=1

    for aux in sorted(n_term):
        name = n_term[aux].insert_type.subtype[:6]
        title_cell_skip = 0
        for i in range(21):
            if i==0:
                r_buffer.append([None, name, title_cell_skip,['insert','insertion',n_term[aux]]])
            else:
                if i<len(name):
                    title_cell_skip = 1
                else:
                    title_cell_skip = 0
                r_buffer.append([None, False, title_cell_skip,['insert','insertion',n_term[aux]]])
        r_chunks_schematic_construct.append(r_buffer)
        r_buffer = []

        ii = 0

    last_segment = False
    a_buffer = []
    nudge = 0
    # create schemtics with annotations
    for i, r in enumerate(residues_custom):
        if r.sequence_number-1 in deletion and i==0:
            r_buffer.append([None, False, 0,annotations[r.sequence_number-1]])
            nudge = 1

        if r.sequence_number+1 in deletion:
            a_buffer.append([ii,annotations[r.sequence_number+1]])

        if (r.protein_segment.slug != last_segment and i!=0) or i == len(residues_custom)-1:
            a_list = {}
            for a in a_buffer:
                temp = a[0]*20 // (ii)
                a_list[temp]  = a[1]
            if (last_segment):
                for a in range(21):
                    if (a-nudge)<len(prev_r.protein_segment.slug):
                        title_cell_skip = 1
                    else:
                        title_cell_skip = 0

                    if a in a_list:
                        annotation = a_list[a]
                    else:
                        annotation = ''

                    if a==0:
                        r_buffer.append([prev_r, prev_r.protein_segment.slug, 0,annotation])
                    else:
                        r_buffer.append([prev_r, False, title_cell_skip,annotation])
                r_chunks_schematic_construct.append(r_buffer)
            last_segment = r.protein_segment.slug
            border = True
            r_buffer = []
            a_buffer = []
            ii = 0
            nudge = 0

        if r.sequence_number in annotations:
            a_buffer.append([ii,annotations[r.sequence_number]])


        if prev_r.sequence_number+1 in insert:
            name = insert[prev_r.sequence_number+1].insert_type.subtype[:6]
            title_cell_skip = 0
            for i in range(21):
                if i==0:
                    r_buffer.append([None, name, title_cell_skip,['insert','insertion',insert[prev_r.sequence_number+1]]])
                else:
                    if i<len(name):
                        title_cell_skip = 1
                    else:
                        title_cell_skip = 0
                    r_buffer.append([None, False, title_cell_skip,['insert','insertion',insert[prev_r.sequence_number+1]]])
            r_chunks_schematic_construct.append(r_buffer)
            r_buffer = []


        if i+1==len(residues_custom) and r.sequence_number+1 in insert:
            name = insert[r.sequence_number+1].insert_type.subtype[:6]
            title_cell_skip = 0
            for i in range(21):
                if i==0:
                    r_buffer.append([None, name, title_cell_skip,['insert','insertion',insert[r.sequence_number+1]]])
                else:
                    if i<len(name):
                        title_cell_skip = 1
                    else:
                        title_cell_skip = 0
                    r_buffer.append([None, False, title_cell_skip,['insert','insertion',insert[r.sequence_number+1]]])
            r_chunks_schematic_construct.append(r_buffer)
            r_buffer = []

        last_segment = r.protein_segment.slug
        prev_r = r
        ii+=1

    # process residues and return them in chunks of 10
    # this is done for easier scaling on smaller screens
    chunk_size = 10
    r_chunks = []
    r_buffer = []
    last_segment = False
    border = False
    title_cell_skip = 0
    for i, r in enumerate(residues):
        # title of segment to be written out for the first residue in each segment
        segment_title = False
        
        # keep track of last residues segment (for marking borders)
        if r.protein_segment.slug != last_segment:
            last_segment = r.protein_segment.slug
            border = True
        
        # if on a border, is there room to write out the title? If not, write title in next chunk
        if i == 0 or (border and len(last_segment) <= (chunk_size - i % chunk_size)):
            segment_title = True
            border = False
            title_cell_skip += len(last_segment) # skip cells following title (which has colspan > 1)
        
        if i and i % chunk_size == 0:
            r_chunks.append(r_buffer)
            r_buffer = []
        
        if r.sequence_number in annotations:
            annotation = annotations[r.sequence_number]
        else:
            annotation = None

        r_buffer.append((r, segment_title, title_cell_skip,annotation))

        # update cell skip counter
        if title_cell_skip > 0:
            title_cell_skip -= 1
    if r_buffer:
        r_chunks.append(r_buffer)

    # process residues and return them in chunks of 10
    # this is done for easier scaling on smaller screens
    r_chunks_custom = []
    r_buffer = []
    last_segment = False
    border = False
    title_cell_skip = 0

    nudge = 0

    fusion = False

    for aux in sorted(n_term):
        name = n_term[aux].insert_type.subtype[:11]
        title_cell_skip = 0
        for i in range(chunk_size):
            if i==0:
                r_buffer.append([None, name, title_cell_skip,['insert','insertion',n_term[aux]]])
            else:
                if i<len(name):
                    title_cell_skip = 1
                else:
                    title_cell_skip = 0
                r_buffer.append([None, False, title_cell_skip,['insert','insertion',n_term[aux]]])
        r_chunks_custom.append(r_buffer)
        r_buffer = []

    title_cell_skip = 0
    for i, r in enumerate(residues_custom):
        # title of segment to be written out for the first residue in each segment
        segment_title = False

        if r.sequence_number-1 in deletion and i==0:
            # r_buffer.append((r, segment_title, title_cell_skip,deletion[r.sequence_number+1]))
            r_buffer.append((None, segment_title, title_cell_skip,deletion[r.sequence_number-1]))
            nudge -= 1
     
        # keep track of last residues segment (for marking borders)
        if r.protein_segment.slug != last_segment:
            last_segment = r.protein_segment.slug
            border = True
        
        # if on a border, is there room to write out the title? If not, write title in next chunk
        if i == 0 or (border and len(last_segment) <= (chunk_size - (i-nudge) % chunk_size)):
            segment_title = True
            border = False
            title_cell_skip += len(last_segment) # skip cells following title (which has colspan > 1)
        
        if len(r_buffer) and i and (i-nudge) % chunk_size == 0:
            r_chunks_custom.append(r_buffer)
            r_buffer = []
        
        if r.sequence_number in annotations:
            annotation = annotations[r.sequence_number]
        else:
            annotation = None
        r_buffer.append((r, segment_title, title_cell_skip,annotation))

        if r.sequence_number+1 in deletion:
            # r_buffer.append((r, segment_title, title_cell_skip,deletion[r.sequence_number+1]))
            r_buffer.append((None, segment_title, title_cell_skip,deletion[r.sequence_number+1]))
            if title_cell_skip > 0: title_cell_skip -=1
            nudge -= 1

        if r.sequence_number+1 in insert:
                if len(r_buffer):
                    r_chunks_custom.append(r_buffer)
                r_buffer = []
                # for _ in range(chunk_size):
                #     r_buffer.append([r, segment_title, title_cell_skip,['insert','insertion']])
                for a in range(chunk_size):
                    name = insert[r.sequence_number+1].insert_type.subtype[:11]
                    if a==0:
                        r_buffer.append([r, name, title_cell_skip,['insert','insertion',insert[r.sequence_number+1]]])
                    else:
                        if a<len(name):
                            title_cell_skip = 1
                        else:
                            title_cell_skip = 0
                        r_buffer.append([r, False, title_cell_skip,['insert','insertion',insert[r.sequence_number+1]]])
                r_chunks_custom.append(r_buffer)
                r_buffer = []
                nudge = ((i+nudge) % chunk_size)+1

        # update cell skip counter
        if title_cell_skip > 0:
            title_cell_skip -= 1
    if r_buffer:
        r_chunks_custom.append(r_buffer)

    context = {'c':c,'r_chunks': r_chunks, 'r_chunks_schematic':r_chunks_schematic, 'r_chunks_custom': r_chunks_custom, 'r_chunks_schematic_construct':r_chunks_schematic_construct, 'chunk_size': chunk_size, 'residues_lookup': residues_lookup}
    return render(request,'construct/construct_detail.html',context)

class ConstructBrowser(TemplateView):
    """
    Fetching construct data for browser
    """

    template_name = "construct_browser.html"

    def get_context_data (self, **kwargs):

        context = super(ConstructBrowser, self).get_context_data(**kwargs)
        try:
            context['constructs'] = Construct.objects.all().prefetch_related(
                "crystal","mutations","purification")
        except Construct.DoesNotExist as e:
            pass

        return context
