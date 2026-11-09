import type { Cliente } from '../../domain/models/cliente';
import type {
  Mascota,
  MascotaConDueno,
  MascotaCreate,
} from '../../domain/models/mascota';
import {
  actualizarMascota,
  crearMascota,
} from '../../infrastructure/api/mascotaService';

export const PREDEFINED_SPECIES = [
  'Perro',
  'Gato',
  'Ave',
  'Roedor',
  'Reptil',
  'Pez',
  'Anfibio',
  'Exotico',
];

const LS_CUSTOM_SPECIES = 'vetpets_custom_species';
const LS_CUSTOM_BREEDS = 'vetpets_custom_breeds_';

export const breedsBySpecies: Record<string, string[]> = {
  Perro: [
    'Mestizo', 'Labrador Retriever', 'Golden Retriever', 'Pastor Aleman', 'Bulldog Ingles', 'Bulldog Frances',
    'Poodle', 'Chihuahua', 'Rottweiler', 'Husky Siberiano', 'Beagle', 'Yorkshire Terrier', 'Schnauzer',
    'Pit Bull', 'American Bully', 'Boxer', 'Dalmata', 'Cocker Spaniel', 'Pug', 'Doberman', 'Shih Tzu',
    'Basset Hound', 'Border Collie', 'Boston Terrier', 'Bull Terrier', 'Caniche', 'Chow Chow',
    'Dogo Argentino', 'Fila Brasileiro', 'Fox Terrier', 'Gran Danes', 'Jack Russell', 'Maltipoo',
    'Maltes', 'Mastin Napolitano', 'Papillon', 'Pastor Australiano', 'Pastor Belga', 'Pekines',
    'Pointer', 'Pomerania', 'Rhodesian Ridgeback', 'Samoyedo', 'San Bernardo', 'Shar Pei',
    'Setter Irlandes', 'Shiba Inu', 'Springer Spaniel', 'Staffordshire', 'Terranova', 'Weimaraner',
    'Welsh Corgi', 'West Highland', 'Xoloitzcuintle',
  ],
  Gato: [
    'Mestizo', 'Siames', 'Persa', 'Maine Coon', 'Bengali', 'Ragdoll', 'Britanico de Pelo Corto',
    'Abisinio', 'Sphynx', 'Scottish Fold', 'Angora Turco', 'Birmano', 'Bombay', 'Burmese', 'Chartreux',
    'Cornish Rex', 'Devon Rex', 'Exotico de Pelo Corto', 'Himalayo', 'Manx', 'Noruego del Bosque',
    'Oriental', 'Ruso Azul', 'Savannah', 'Singapura', 'Somali', 'Tonkines', 'Van Turco',
  ],
  Ave: [
    'Periquito Australiano', 'Canario', 'Loro Amazonas', 'Cacatua', 'Agaporni', 'Cotorra Argentina',
    'Guacamaya', 'Ninfa', 'Calopsita', 'Diamante Mandarin', 'Jilguero', 'Pinzon', 'Cardenal',
    'Paloma', 'Codorniz', 'Faisán', 'Pavo Real', 'Gallina', 'Pato', 'Ganso', 'Tucan', 'Loro Gris Africano',
    'Eclectus', 'Caique', 'Quaker', 'Loro Senegalés',
  ],
  Roedor: [
    'Hamster Sirio', 'Hamster Ruso', 'Hamster Roborovski', 'Cobaya', 'Conejo Holandes', 'Conejo Belier',
    'Conejo Rex', 'Conejo Angora', 'Conejo Cabeza de Leon', 'Rata Domestica', 'Raton Domestico',
    'Chinchilla', 'Huron', 'Jerbo', 'Ardilla de Richardson', 'Degú', 'Erizo Africano',
  ],
  Reptil: [
    'Iguana Verde', 'Tortuga de Orejas Rojas', 'Tortuga Rusa', 'Tortuga Sulcata', 'Gecko Leopardo',
    'Gecko Crestado', 'Dragon Barbudo', 'Python Ball', 'Boa Constrictor', 'Serpiente del Maiz',
    'Camaleon Velado', 'Camaleon Pantera', 'Monitor de Sabana', 'Tegu Argentino', 'Tortuga de Caja',
    'Tortuga Mora', 'Axolotl', 'Salamandra',
  ],
  Pez: [
    'Betta', 'Goldfish', 'Guppy', 'Molly', 'Platy', 'Tetra Neon', 'Pez Angel', 'Disco', 'Oscar',
    'Cichilido', 'Corydora', 'Pleco', 'Pez Payaso', 'Pez Cirujano', 'Pez Damisela', 'Pez Globo',
    'Carpa Koi', 'Pez Bichir',
  ],
  Anfibio: [
    'Rana Arboricola', 'Rana Africana', 'Sapo Comun', 'Axolotl', 'Salamandra de Fuego',
    'Triton Japones', 'Rana Punta de Flecha', 'Sapo de Caña',
  ],
  Exotico: [
    'Mono Capuchino', 'Mono Titi', 'Sugar Glider', 'Perezoso', 'Mapache', 'Coati', 'Kinkaju',
    'Feneco', 'Zorro', 'Mofeta', 'Armadillo', 'Capibaraa', 'Mini Pig', 'Cabra Enana',
  ],
};

export const speciesEmojis: Record<string, string> = {
  Perro: '🐕',
  Gato: '🐱',
  Ave: '🦜',
  Roedor: '🐹',
  Reptil: '🦎',
  Pez: '🐠',
  Anfibio: '🐸',
  Exotico: '🦥',
  Otro: '🐾',
};

export const speciesColors: Record<string, string> = {
  Perro: 'bg-amber-500/20',
  Gato: 'bg-purple-500/20',
  Ave: 'bg-sky-500/20',
  Roedor: 'bg-pink-500/20',
  Reptil: 'bg-lime-500/20',
  Pez: 'bg-cyan-500/20',
  Anfibio: 'bg-green-500/20',
  Exotico: 'bg-orange-500/20',
  Otro: 'bg-gray-500/20',
};

export const speciesBadgeColors: Record<string, string> = {
  Perro: 'bg-amber-500/20 text-amber-300',
  Gato: 'bg-purple-500/20 text-purple-300',
  Ave: 'bg-sky-500/20 text-sky-300',
  Roedor: 'bg-pink-500/20 text-pink-300',
  Reptil: 'bg-lime-500/20 text-lime-300',
  Pez: 'bg-cyan-500/20 text-cyan-300',
  Anfibio: 'bg-green-500/20 text-green-300',
  Exotico: 'bg-orange-500/20 text-orange-300',
  Otro: 'bg-gray-500/20 text-gray-300',
};

export function getCustomSpecies(): string[] {
  try {
    return JSON.parse(localStorage.getItem(LS_CUSTOM_SPECIES) || '[]');
  } catch {
    return [];
  }
}

export function saveCustomSpeciesList(list: string[]): void {
  localStorage.setItem(LS_CUSTOM_SPECIES, JSON.stringify(list));
}

export function getCustomBreeds(species: string): string[] {
  try {
    return JSON.parse(localStorage.getItem(LS_CUSTOM_BREEDS + species) || '[]');
  } catch {
    return [];
  }
}

export function saveCustomBreedsList(species: string, list: string[]): void {
  localStorage.setItem(LS_CUSTOM_BREEDS + species, JSON.stringify(list));
}

export function getBreedsForSpecies(species: string): string[] {
  const predefined = breedsBySpecies[species] || [];
  const custom = getCustomBreeds(species);
  return [...predefined, ...custom.filter((b) => !predefined.includes(b))];
}

export function persistCustomSpeciesToStorage(especie: string): boolean {
  if (!especie || PREDEFINED_SPECIES.includes(especie)) return false;
  const list = getCustomSpecies();
  if (list.includes(especie)) return false;
  list.push(especie);
  saveCustomSpeciesList(list);
  return true;
}

export function persistCustomBreedToStorage(especie: string, raza: string): void {
  if (!especie || !raza) return;
  const predefined = breedsBySpecies[especie] || [];
  const custom = getCustomBreeds(especie);
  if (predefined.includes(raza) || custom.includes(raza)) return;
  custom.push(raza);
  saveCustomBreedsList(especie, custom);
}

/**
 * Construye la cadena de edad ("X años Y meses") a partir de los campos del formulario.
 */
export function buildMascotaEdad(
  edadAnios?: string,
  edadMeses?: string
): string | undefined {
  let edadStr = '';
  if (edadAnios && parseInt(edadAnios, 10) > 0) {
    const anios = parseInt(edadAnios, 10);
    edadStr = `${anios} año${anios > 1 ? 's' : ''}`;
  }
  if (edadMeses && parseInt(edadMeses, 10) > 0) {
    const meses = parseInt(edadMeses, 10);
    if (edadStr) edadStr += ' ';
    edadStr += `${meses} mes${meses > 1 ? 'es' : ''}`;
  }
  return edadStr || undefined;
}

/**
 * Descompone la cadena de edad en años y meses para edición en el formulario.
 */
export function parseMascotaEdad(edadStr?: string): { anios: string; meses: string } {
  const raw = edadStr || '';
  const aniosMatch = raw.match(/(\d+)\s*años?/i);
  const mesesMatch = raw.match(/(\d+)\s*mes(es)?/i);
  return {
    anios: aniosMatch ? aniosMatch[1] : '',
    meses: mesesMatch ? mesesMatch[1] : '',
  };
}

/**
 * Descompone la cadena de peso en valor y unidad ("kg" | "g").
 */
export function parseMascotaPeso(pesoStr?: string): { valor: string; unidad: string } {
  const pesoMatch = (pesoStr || '').match(/^([\d.]+)\s*(kg|g)?$/i);
  if (!pesoMatch) return { valor: '', unidad: 'kg' };
  return {
    valor: pesoMatch[1],
    unidad: pesoMatch[2]?.toLowerCase() || 'kg',
  };
}

/**
 * Filtra clientes para el autocompletado de dueño en el formulario de mascotas.
 */
export function filterClientesAutocomplete(
  clients: Cliente[],
  term: string,
  searchType: string
): Cliente[] {
  const cleanTerm = (term || '').trim();
  if (!cleanTerm) return [];

  return clients
    .filter((c) => {
      if (searchType === 'id') {
        return c.id.toString() === cleanTerm;
      }
      if (searchType === 'telefono') {
        const digitsOnly = cleanTerm.replace(/\D/g, '');
        return c.telefono.replace(/\D/g, '').includes(digitsOnly);
      }
      return c.nombre.toLowerCase().includes(cleanTerm.toLowerCase());
    })
    .slice(0, 8);
}

/**
 * Filtra la lista de mascotas según término de búsqueda, especie y cliente.
 */
export function filterMascotas(
  pets: MascotaConDueno[],
  params: {
    searchTerm: string;
    searchType: string;
    species: string;
    clientId: string;
  }
): MascotaConDueno[] {
  const searchTerm = (params.searchTerm || '').trim();
  const searchTermLower = searchTerm.toLowerCase();

  return pets.filter((pet) => {
    let matchesSearch = true;
    if (searchTerm) {
      switch (params.searchType) {
        case 'id':
          matchesSearch = pet.id.toString() === searchTerm;
          break;
        case 'nombre':
          matchesSearch = pet.nombre.toLowerCase().includes(searchTermLower);
          break;
        default:
          matchesSearch =
            pet.id.toString() === searchTerm ||
            pet.nombre.toLowerCase().includes(searchTermLower);
      }
    }
    const matchesSpecies = !params.species || pet.especie === params.species;
    const matchesClient =
      !params.clientId || pet.cliente_id === parseInt(params.clientId, 10);
    return matchesSearch && matchesSpecies && matchesClient;
  });
}

export interface MascotaFormInput {
  petId?: string | number | null;
  clienteIdStr: string;
  nombre: string;
  especie: string;
  raza?: string;
  edadAnios?: string;
  edadMeses?: string;
  pesoValor?: string;
  pesoUnidad?: string;
  notas?: string;
}

/**
 * Caso de uso: Validar y guardar (crear o actualizar) una mascota.
 */
export async function guardarMascotaUseCase(
  input: MascotaFormInput
): Promise<Mascota> {
  if (!input.clienteIdStr || !String(input.clienteIdStr).trim()) {
    throw new Error('Debes seleccionar un dueño');
  }

  const clienteId = parseInt(String(input.clienteIdStr), 10);
  const edad = buildMascotaEdad(input.edadAnios, input.edadMeses);
  const peso = input.pesoValor
    ? `${input.pesoValor} ${input.pesoUnidad || 'kg'}`
    : undefined;

  const data: MascotaCreate = {
    nombre: input.nombre.trim(),
    especie: input.especie.trim(),
    raza: input.raza?.trim() || undefined,
    edad,
    peso,
    notas: input.notas?.trim() || undefined,
  };

  const numericPetId =
    typeof input.petId === 'number'
      ? input.petId
      : input.petId && String(input.petId).trim()
      ? parseInt(String(input.petId), 10)
      : null;

  const saved = numericPetId
    ? await actualizarMascota(numericPetId, data)
    : await crearMascota(clienteId, data);

  persistCustomSpeciesToStorage(data.especie);
  if (data.raza) {
    persistCustomBreedToStorage(data.especie, data.raza);
  }

  return saved;
}

